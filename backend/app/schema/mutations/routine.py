import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Routine, Product, User
from app.schema.types import RoutineType

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    category = graphene.String(required=True)
    time_of_use = graphene.String(required=True)

class CreateRoutine(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        products = graphene.List(ProductInput)

    success = graphene.Boolean()
    routine = graphene.Field(lambda: RoutineType)

    @jwt_required()
    def mutate(self, info, name, description=None, products=None):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        if not user:
            raise Exception("User not found")

        # Create Routine
        routine = Routine(name=name, description=description, user_id=user.id)
        db.session.add(routine)
        db.session.commit()

        # Add Products
        if products:
            for product_data in products:
                product = Product(
                    name=product_data.name,
                    category=product_data.category,
                    time_of_use=product_data.time_of_use,
                    user_id=user.id  # <-- this is required
                )
                routine.products.append(product)
                db.session.add(product)

        db.session.commit()

        return CreateRoutine(success=True, routine=routine)

class RemoveProductFromRoutine(graphene.Mutation):
    class Arguments:
        routine_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)

    success = graphene.Boolean()
    routine = graphene.Field(lambda: RoutineType)

    @jwt_required()
    def mutate(self, info, routine_id, product_id):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if not user:
            raise Exception("User not found")

        routine = Routine.query.filter_by(id=routine_id, user_id=user.id).first()

        if not routine:
            raise Exception("Routine not found or unauthorized")

        product = Product.query.get(product_id)
        if not product:
            raise Exception("Product not found")

        if product in routine.products:
            routine.products.remove(product)
            db.session.commit()
            return RemoveProductFromRoutine(success=True, routine=routine)

        return RemoveProductFromRoutine(success=False, routine=routine)
    
class AddProductToRoutine(graphene.Mutation):
    class Arguments:
        routine_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        category = graphene.String(required=True)
        time_of_use = graphene.String(required=True)

    success = graphene.Boolean()
    routine = graphene.Field(lambda: RoutineType)

    @jwt_required()
    def mutate(self, info, routine_id, name, category, time_of_use):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if not user:
            raise Exception("User not found")

        routine = Routine.query.filter_by(id=routine_id, user_id=user.id).first()

        if not routine:
            raise Exception("Routine not found or unauthorized")

        # Create and link product
        product = Product(
            name=name,
            category=category,
            time_of_use=time_of_use,
            user_id=user.id
        )

        routine.products.append(product)
        db.session.add(product)
        db.session.commit()

        return AddProductToRoutine(success=True, routine=routine)

class DeleteRoutine(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if not user:
            raise Exception("User not found")

        routine = Routine.query.filter_by(id=id, user_id=user.id).first()

        if not routine:
            raise Exception("Routine not found or unauthorized")

        # Collect associated products
        products = list(routine.products)

        # Remove associations first
        routine.products.clear()
        db.session.flush()

        # Then delete each product (optional: check if shared across routines)
        for product in products:
            db.session.delete(product)

        # Finally, delete the routine itself
        db.session.delete(routine)
        db.session.commit()

        return DeleteRoutine(success=True)
    # Add this after the DeleteRoutine class

class EditRoutine(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
        description = graphene.String()

    success = graphene.Boolean()
    routine = graphene.Field(lambda: RoutineType)

    @jwt_required()
    def mutate(self, info, id, name, description=None):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if not user:
            raise Exception("User not found")

        routine = Routine.query.filter_by(id=id, user_id=user.id).first()

        if not routine:
            raise Exception("Routine not found or unauthorized")

        routine.name = name
        routine.description = description
        db.session.commit()

        return EditRoutine(success=True, routine=routine)