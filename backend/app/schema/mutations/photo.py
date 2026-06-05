import graphene
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Photo, Analysis
from graphene_file_upload.scalars import Upload
from app.schema.types import AnalysisType
from flask import Flask
import os
import base64
from app.models import User
from app.AIScript.face_analysis import analyze_face
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class UploadPhoto(graphene.Mutation):
    class Arguments:
        photo = Upload(required=True)

    id = graphene.Int()
    imageUrl = graphene.String()
    analysis = graphene.Field(AnalysisType)

    @jwt_required()
    def mutate(self, info, photo, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.filter_by(email=user_id).first()
        logging.debug(f"User:user.id")
        if not user:
            raise Exception("User not authenticated!")

        session = db.session
        photo_content = photo.read()
        file_path = f"uploads/{photo.filename}"

        full_path = os.path.join(UPLOAD_DIR, photo.filename)

        with open(full_path, "wb") as f:
            f.write(photo_content)

        new_photo = Photo(user_id=user.id, photo_link=file_path, image_blob=photo_content)
        session.add(new_photo)
        session.commit()

        data = analyze_face(base64.b64encode(new_photo.image_blob))
        if "error" in data:
            raise Exception(data["error"])

        print(data)
        new_analysis = Analysis(photo_id=new_photo.id, age=str(data['age']), hydration=str(data['hydration']), fine_lines=str(data['fine_lines']), texture=str(data['texture']), is_complete=True)
        session.add(new_analysis)
        session.commit()

        return UploadPhoto(id=new_photo.id, imageUrl=new_photo.photo_link)
    
    def resolve_image_b64(self, info):
        """Convert image blob to Base64 for API response"""
        logging.debug("info: ",info)
        return base64.b64encode(self.image_blob).decode('utf-8') if self.image_blob else None

class DeleteAnalysis(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @jwt_required()
    def mutate(self, info, id):
        try:
            # Get current user
            user_id = get_jwt_identity()
            user = User.query.filter_by(email=user_id).first()
            
            if not user:
                return DeleteAnalysis(success=False, message="Not authenticated")

            # Find analysis and check ownership
            analysis = Analysis.query.join(Photo).filter(
                Analysis.id == id,
                Photo.user_id == user.id
            ).first()

            if not analysis:
                return DeleteAnalysis(
                    success=False,
                    message="Analysis not found or unauthorized"
                )

            # Delete the analysis
            db.session.delete(analysis)
            db.session.commit()

            return DeleteAnalysis(success=True, message="Analysis deleted successfully")

        except Exception as e:
            db.session.rollback()
            print(f"Error deleting analysis: {e}")
            return DeleteAnalysis(success=False, message="Failed to delete analysis")
