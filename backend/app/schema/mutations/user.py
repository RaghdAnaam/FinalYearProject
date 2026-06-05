import graphene
from app.models import db, User
from flask_jwt_extended import create_access_token
from app.schema.types import UserType
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils.email_utils import send_reset_email, send_reset_email_brevo
from .utils.token_utils import generate_reset_token, verify_reset_token

class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, first_name, last_name, email, password):
        if User.query.filter_by(email=email).first():
            return CreateUser(user=None, success=False, message="Email already registered.")

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
            )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return CreateUser(user=new_user, success=True, message="User created successfully.")
        except Exception as e:
            db.session.rollback()
            return CreateUser(user=None, success=False, message=str(e))

class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email, password):
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            db.session.commit()

            token = create_access_token(identity=user.email)
            return Login(token=token, success=True, message="Login successful.")

        return Login(token=None, success=False, message="Invalid credentials.")

class DeleteUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @jwt_required()
    def mutate(self, info, email):
        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()

        if not current_user:
            return DeleteUser(success=False, message="Authenticated user not found.")

        target_user = User.query.filter_by(email=email).first()

        if not target_user:
            return DeleteUser(success=False, message="User not found.")

        try:
            db.session.delete(target_user)
            db.session.commit()
            return DeleteUser(success=True, message="User deleted successfully.")
        except Exception as e:
            db.session.rollback()
            return DeleteUser(success=False, message=f"Failed to delete user: {str(e)}")

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)             # Target user ID
        email = graphene.String()                    # Can now update email
        first_name = graphene.String()
        last_name = graphene.String()
        password = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)

    @jwt_required()
    def mutate(self, info, id, email=None, first_name=None, last_name=None, password=None):
        current_user_email = get_jwt_identity()
        admin_user = User.query.filter_by(email=current_user_email).first()

        if not admin_user:
            return UpdateUser(success=False, message="Authenticated user not found.")

        user = User.query.get(id)
        if not user:
            return UpdateUser(success=False, message="Target user not found.")

        try:
            if email is not None:
                existing = User.query.filter_by(email=email).first()
                if existing and existing.id != user.id:
                    return UpdateUser(success=False, message="Email already in use.")
                user.email = email

            if first_name is not None:
                user.first_name = first_name

            if last_name is not None:
                user.last_name = last_name

            if password is not None:
                user.set_password(password)

            db.session.commit()
            return UpdateUser(success=True, message="User updated successfully.", user=user)

        except Exception as e:
            db.session.rollback()
            return UpdateUser(success=False, message=f"Failed to update user: {str(e)}", user=None)

class RequestPasswordReset(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return RequestPasswordReset(success=False, message="If that email exists, a reset link will be sent.")

        token = generate_reset_token(user.email)
        try:
            send_reset_email_brevo(user.email, token)
            return RequestPasswordReset(success=True, message="Check your email for reset link.")
        except Exception as e:
            return RequestPasswordReset(success=False, message=str(e))


class ResetPassword(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, token, new_password):
        email = verify_reset_token(token)
        if not email:
            return ResetPassword(success=False, message="Invalid or expired token.")

        user = User.query.filter_by(email=email).first()
        if not user:
            return ResetPassword(success=False, message="User not found.")

        user.set_password(new_password)
        db.session.commit()
        return ResetPassword(success=True, message="Password updated successfully.")
    
   

class UpdateProfile(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(name='firstName')   # <- Important!
        last_name = graphene.String(name='lastName')
        email = graphene.String()
        password = graphene.String()

    success = graphene.Boolean()
    user = graphene.Field(lambda: UserType)
    message = graphene.String()
    token = graphene.String()  # NEW: Return new token if email changed

    def mutate(self, info, first_name=None, last_name=None, email=None, password=None):

        user_email = info.context.get('user')
        if not user_email:
            raise GraphQLError("Not authenticated")

        user = User.query.filter_by(email=user_email).first()
        if not user:
            raise GraphQLError("User not found")

        new_token = None

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        # Email update (with token re-issue)
        if email and email != user.email:
            if User.query.filter_by(email=email).first():
                raise GraphQLError("Email already exists")
            user.email = email
            new_token = create_access_token(identity=email)  # NEW

        # Password update
        if password and password.strip():
            user.set_password(password)

        try:
            db.session.commit()
            return UpdateProfile(
                success=True, 
                user=user,
                message="Profile updated successfully.",
                token=new_token
            )
        except Exception as e:
            db.session.rollback()
            return UpdateProfile(success=False, message=str(e), user=None, token=None)
