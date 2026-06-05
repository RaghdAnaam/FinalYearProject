import graphene
import math
from base64 import b64encode
import logging
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from graphql import GraphQLError
from app.models import User, Product, Report, Routine, Photo, Analysis, Admin, db
from app.schema.types import (
    UserType, ProductType, ReportType, RoutineType, PhotoType,
    AnalysisType, AdminType, MetricsType
)

# Configure logging if not already configured
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class PaginatedUsersType(graphene.ObjectType):
    users = graphene.List(UserType)
    total = graphene.Int()
    pages = graphene.Int()
    page = graphene.Int()
    per_page = graphene.Int()


class Query(graphene.ObjectType):
    all_users = graphene.Field(
        PaginatedUsersType,
        page=graphene.Int(default_value=1),
        per_page=graphene.Int(default_value=10)
    )
    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))
    all_products = graphene.List(ProductType)
    all_reports = graphene.List(ReportType)
    all_routines = graphene.List(RoutineType)
    my_photos_with_analyses = graphene.List(PhotoType)
    my_routines = graphene.List(RoutineType)
    user_photos = graphene.List(PhotoType)
    all_admins = graphene.List(AdminType)
    admin_by_id = graphene.Field(AdminType, id=graphene.Int(required=True))
    metrics = graphene.Field(MetricsType)
    search_users = graphene.Field(
        PaginatedUsersType,
        search=graphene.String(required=True),
        page=graphene.Int(default_value=1),
        per_page=graphene.Int(default_value=10)
    )
    # ---- Added for profile icon/user info ----
    current_user = graphene.Field(UserType)

    @staticmethod
    def get_current_user(info):
        user_email = info.context.get("user")
        if not user_email:
            raise GraphQLError("Authentication required")
        user = User.query.filter_by(email=user_email).first()
        if not user:
            raise GraphQLError("User not found")
        return user

    @staticmethod
    def require_admin(user):
        if not isinstance(user, Admin):
            raise GraphQLError("Access denied: Admins only.")

    def resolve_all_users(self, info, page=1, per_page=10):
        user = Query.get_current_user(info)
        Query.require_admin(user)

        admin_subquery = db.session.query(Admin.id).subquery()
        query = User.query.filter(~User.id.in_(admin_subquery))
        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()

        return PaginatedUsersType(
            users=users,
            total=total,
            pages=math.ceil(total / per_page),
            page=page,
            per_page=per_page
        )

    def resolve_user_by_id(self, info, id):
        user = Query.get_current_user(info)
        Query.require_admin(user)
        return User.query.get(id)

    def resolve_all_products(self, info):
        user = Query.get_current_user(info)
        Query.require_admin(user)
        return Product.query.all()

    def resolve_all_reports(self, info):
        user = Query.get_current_user(info)
        Query.require_admin(user)
        return Report.query.all()

    def resolve_all_routines(self, info):
        user = Query.get_current_user(info)
        Query.require_admin(user)
        return Routine.query.all()

    def resolve_all_admins(self, info):
        user = Query.get_current_user(info)
        Query.require_admin(user)
        return Admin.query.all()

    def resolve_admin_by_id(self, info, id):
        user = Query.get_current_user(info)
        Query.require_admin(user)
        return Admin.query.get(id)

    def resolve_my_photos_with_analyses(self, info):
        user = Query.get_current_user(info)
        photos = (
            Photo.query.options(joinedload(Photo.analysis))
            .filter_by(user_id=user.id)
            .all()
        )
        for photo in photos:
            for analysis in photo.analysis:
                if isinstance(analysis.texture, bytes):
                    analysis.texture = b64encode(analysis.texture).decode("utf-8")
        return photos

    def resolve_user_photos(self, info):
        user = Query.get_current_user(info)
        return Photo.query.filter_by(user_id=user.id).all()

    def resolve_my_routines(self, info):
        user = Query.get_current_user(info)
        return Routine.query.filter_by(user_id=user.id).all()

    def resolve_metrics(self, info):
        try:
            # Authenticate and authorize user
            user = Query.get_current_user(info)
            Query.require_admin(user)
            
            # Log the metrics request
            logging.info(f"Metrics requested by admin: {user.email}")
            
            # Create subquery for admin filtering
            admin_subquery = db.session.query(Admin.id).subquery()
            
            # Get total users (excluding admins)
            total_users = User.query.filter(
                ~User.id.in_(admin_subquery)
            ).count()
            
            # Calculate active users in last 30 days
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            active_users = User.query.filter(
                ~User.id.in_(admin_subquery),
                User.last_login.isnot(None),
                User.last_login >= thirty_days_ago
            ).count()
            
            # Validate metrics
            if total_users < 0 or active_users < 0:
                logging.error(f"Invalid metrics values: total={total_users}, active={active_users}")
                raise GraphQLError("Invalid metrics values detected")
                
            if active_users > total_users:
                logging.error(f"Active users ({active_users}) greater than total users ({total_users})")
                raise GraphQLError("Inconsistent metrics values detected")
            
            # Log the metrics results
            logging.debug(f"Metrics calculated - Total: {total_users}, Active: {active_users}")
            
            return MetricsType(
                total_users=total_users,
                active_users_last_30_days=active_users
            )
            
        except GraphQLError as e:
            # Re-raise GraphQL specific errors
            raise
            
        except Exception as e:
            # Log unexpected errors and return a generic error message
            logging.error(f"Error calculating metrics: {str(e)}", exc_info=True)
            raise GraphQLError("Failed to calculate metrics. Please try again later.")

    def resolve_search_users(self, info, search, page=1, per_page=10):
        user = Query.get_current_user(info)
        Query.require_admin(user)

        admin_subquery = db.session.query(Admin.id).subquery()
        query = User.query.filter(
            ~User.id.in_(admin_subquery),
            (
                User.first_name.ilike(f"%{search}%") |
                User.last_name.ilike(f"%{search}%") |
                User.email.ilike(f"%{search}%")
            )
        )

        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()

        return PaginatedUsersType(
            users=users,
            total=total,
            pages=math.ceil(total / per_page),
            page=page,
            per_page=per_page
        )
    
    # ---- Add this at the end of your Query class ----
    def resolve_current_user(self, info):
        user_email = info.context.get("user")
        if not user_email:
            raise GraphQLError("Authentication required")
        user = User.query.filter_by(email=user_email).first()
        if not user:
            raise GraphQLError("User not found")
        return user
