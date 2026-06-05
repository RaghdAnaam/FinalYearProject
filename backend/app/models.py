from app import db
import enum
from sqlalchemy import ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }

    photos = relationship("Photo", back_populates="user", cascade="all, delete-orphan")
    skin_progress = relationship("SkinProgress", back_populates="user", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    routines = relationship("Routine", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class AdminRankEnum(enum.Enum):
    head_admin = "head_admin"
    customer_support_admin = "customer_support_admin"
    moderator = "moderator"

class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    can_generate_reports = db.Column(db.Boolean, default=True)
    can_manage_users = db.Column(db.Boolean, default=True)
    can_manage_admins = db.Column(db.Boolean, default=True)  # Fixed typo from 'caqnm'
    can_delete_data = db.Column(db.Boolean, default=False)

    admin_rank = db.Column(SqlEnum(AdminRankEnum, name="admin_rank_enum"), nullable=False, default=AdminRankEnum.moderator)


class Photo(db.Model):
    __tablename__ = "photo"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    photo_link = db.Column(db.String(255), nullable=True)
    image_blob = db.Column(db.LargeBinary, nullable=True)
    date = db.Column(db.DATE, default=func.current_date(), nullable=False)
    time = db.Column(db.TIME, default=func.current_time(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="photos")
    analysis = relationship("Analysis", back_populates="photo", cascade="all, delete-orphan")


class Analysis(db.Model):
    __tablename__ = "analysis"

    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, ForeignKey("photo.id", ondelete="CASCADE"), nullable=False)
    age = db.Column(db.String(255),nullable=True)
    hydration = db.Column(db.String(255),nullable=True)
    fine_lines = db.Column(db.String(255),nullable=True)
    texture = db.Column(db.String(255),nullable=True)
    is_complete = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.DATE, default=func.current_date(), nullable=False)

    # Relationships
    photo = relationship("Photo", back_populates="analysis")


class SkinProgress(db.Model):
    __tablename__ = "skin_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    progress_score = db.Column(db.Integer, nullable=False)

    user = relationship("User", back_populates="skin_progress")


routine_products = db.Table(
    "routine_products",
    db.Column("routine_id", db.Integer, ForeignKey("routine.id", ondelete="CASCADE"), primary_key=True),
    db.Column("product_id", db.Integer, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
)


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    time_of_use = db.Column(db.String(255), nullable=False)

    user = relationship("User", back_populates="products")
    routines = relationship("Routine", secondary=routine_products, back_populates="products")


class Report(db.Model):
    __tablename__ = "report"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    start_date = db.Column(db.DATE, nullable=False)
    end_date = db.Column(db.DATE, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    report_link = db.Column(db.String(255), nullable=False)

    # Relationships
    user = relationship("User", back_populates="reports")


class Routine(db.Model):
    __tablename__ = "routine"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="routines")
    products = relationship("Product", secondary=routine_products, back_populates="routines")
