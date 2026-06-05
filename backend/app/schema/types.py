import graphene
import base64
from app import db 
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import User, Photo, Analysis, SkinProgress, Product, Report, Routine, Admin

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        include_relationships = True
        metadata = db.metadata  # ✅ Add this line

class AdminType(UserType):  # Inherits from UserType
    class Meta:
        model = Admin
        include_relationships = True
        metadata = db.metadata

    can_generate_reports = graphene.Boolean()
    can_manage_users = graphene.Boolean()
    can_delete_data = graphene.Boolean()
    
class PhotoType(SQLAlchemyObjectType):
    class Meta:
        model = Photo
    date = graphene.Date()
    image_b64 = graphene.String()
    user_id = graphene.Int()  # Ensure user_id is explicitly an integer


    def resolve_image_b64(self, info):
        return base64.b64encode(self.image_blob).decode('utf-8') if self.image_blob else None


class AnalysisType(SQLAlchemyObjectType):
    class Meta:
        model = Analysis
        include_relationships = True

    result = graphene.String()
    created_at = graphene.DateTime()

class SkinProgressType(SQLAlchemyObjectType):
    class Meta:
        model = SkinProgress

class ProductType(SQLAlchemyObjectType):
    class Meta:
        model = Product

    category = graphene.String()
    timeOfUse = graphene.String()
    
    def resolve_timeOfUse(parent, info):
        return parent.time_of_use


class ReportType(SQLAlchemyObjectType):
    class Meta:
        model = Report

class RoutineType(SQLAlchemyObjectType):
    class Meta:
        model = Routine
        include_relationships = True  # ✅ Ensure relationships are included

    products = graphene.List(lambda: ProductType)  # ✅ Explicitly add products relationship

    def resolve_products(self, info):
        return self.products  # ✅ Return related products


class MetricsType(graphene.ObjectType):
    total_users = graphene.Int()
    active_users_last_30_days = graphene.Int()