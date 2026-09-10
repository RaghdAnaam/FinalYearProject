from flask import Blueprint
import os
from flask import make_response, request
from flask_cors import CORS
from graphene_file_upload.flask import FileUploadGraphQLView
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.schema import schema
import logging

graphql_bp = Blueprint("graphql", __name__)

# ✅ Let flask-cors handle everything properly
ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173,https://skin-vision-brown.vercel.app").split(",") if origin.strip()]
CORS(graphql_bp, origins=ALLOWED_ORIGINS, supports_credentials=True)

@graphql_bp.route("/", methods=["OPTIONS"])
def graphql_options():
    response = make_response()
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers.add("Access-Control-Allow-Origin", origin)
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200
# ✅ Add user to GraphQL context
def add_user_to_context(info):
    try:
        verify_jwt_in_request(optional=True)  # ✅ allow request without token
        user_id = get_jwt_identity()
        info.context.user = user_id
    except Exception as e:
        info.context.user = None  # No token or failed verification
    return info

# ✅ Add GraphQL endpoint with all necessary methods
graphql_bp.add_url_rule(
    "/",
    view_func=FileUploadGraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
        get_context=lambda: get_graphql_context()
    ),
    methods=["GET", "POST", "OPTIONS"]
)

def get_graphql_context():
    try:
        verify_jwt_in_request(optional=True)  # Will raise if invalid token
        user = get_jwt_identity()
    except Exception as e:
        user = None
    return {
        "request": request,
        "user": user
    }