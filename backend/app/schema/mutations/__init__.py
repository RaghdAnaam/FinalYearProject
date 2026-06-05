import graphene
from .user import CreateUser, Login, UpdateUser, DeleteUser, ResetPassword, RequestPasswordReset, UpdateProfile
from .product import CreateProduct
from .report import CreateReport
from .routine import CreateRoutine, EditRoutine, RemoveProductFromRoutine, AddProductToRoutine, DeleteRoutine
from .photo import UploadPhoto, DeleteAnalysis  # Add DeleteAnalysis here
from .admin import CreateAdmin, LoginAdmin

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_product = CreateProduct.Field()
    create_report = CreateReport.Field()
    upload_photo = UploadPhoto.Field()
    login = Login.Field()
    create_routine = CreateRoutine.Field()
    login_admin = LoginAdmin.Field()
    create_admin = CreateAdmin.Field()
    remove_product_from_routine = RemoveProductFromRoutine.Field()
    add_product_to_routine = AddProductToRoutine.Field()
    delete_routine = DeleteRoutine.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()
    update_profile = UpdateProfile.Field()
    edit_routine = EditRoutine.Field()
    delete_analysis = DeleteAnalysis.Field()  # Add this line
