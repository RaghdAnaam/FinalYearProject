import logging
import graphene
from datetime import datetime
from flask_jwt_extended import create_access_token
from app.models import db, User, Admin, AdminRankEnum
from graphql import GraphQLError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreateAdmin(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        can_generate_reports = graphene.Boolean()
        can_manage_users = graphene.Boolean()
        can_manage_admins = graphene.Boolean()
        can_delete_data = graphene.Boolean()
        admin_rank = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(
        self, info,
        first_name, last_name, email, password,
        can_generate_reports=True,
        can_manage_users=True,
        can_manage_admins=True,
        can_delete_data=False,
        admin_rank="moderator"
    ):
        try:
            # Validate email
            if not email or '@' not in email:
                return CreateAdmin(success=False, message="Invalid email format.")

            # Check existing user
            if User.query.filter_by(email=email).first():
                logger.warning(f"Attempted to create admin with existing email: {email}")
                return CreateAdmin(success=False, message="Email already exists.")

            # Validate admin rank
            try:
                rank_enum = AdminRankEnum(admin_rank)
            except ValueError:
                logger.error(f"Invalid admin rank attempted: {admin_rank}")
                return CreateAdmin(success=False, message="Invalid admin rank.")

            # Create admin instance
            admin = Admin(
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                email=email.lower().strip(),
                can_generate_reports=can_generate_reports,
                can_manage_users=can_manage_users,
                can_manage_admins=can_manage_admins,
                can_delete_data=can_delete_data,
                admin_rank=rank_enum
            )

            # Set password and save
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()

            logger.info(f"New admin created: {email}")
            return CreateAdmin(success=True, message="Admin account created successfully.")

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating admin: {str(e)}", exc_info=True)
            return CreateAdmin(success=False, message="Failed to create admin account.")


class LoginAdmin(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email, password):
        try:
            # Input validation
            if not email or not password:
                return LoginAdmin(token=None, success=False, message="Email and password required.")

            user = User.query.filter_by(email=email.lower().strip()).first()

            # Check credentials
            if not user or not user.check_password(password):
                logger.warning(f"Failed login attempt for email: {email}")
                return LoginAdmin(token=None, success=False, message="Invalid credentials.")

            # Verify admin status
            if not isinstance(user, Admin):
                logger.warning(f"Non-admin user attempted admin login: {email}")
                return LoginAdmin(token=None, success=False, message="Access denied: Not an admin.")

            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Create token with admin claims
            token = create_access_token(
                identity=user.email,
                additional_claims={
                    "is_admin": True,
                    "admin_rank": user.admin_rank.value,
                    "permissions": {
                        "can_generate_reports": user.can_generate_reports,
                        "can_manage_users": user.can_manage_users,
                        "can_manage_admins": user.can_manage_admins,
                        "can_delete_data": user.can_delete_data
                    }
                }
            )

            logger.info(f"Admin login successful: {email}")
            return LoginAdmin(token=token, success=True, message="Login successful.")

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during admin login: {str(e)}", exc_info=True)
            return LoginAdmin(token=None, success=False, message="Login failed. Please try again.")
