import graphene
from app.models import db, Product
from app.schema.types import ProductType

class CreateProduct(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        category = graphene.String(required=True)
        time_of_use = graphene.String(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, user_id, name, category, time_of_use):
        new_product = Product(user_id=user_id, name=name, category=category, time_of_use=time_of_use)
        db.session.add(new_product)
        db.session.commit()
        return CreateProduct(product=new_product)
