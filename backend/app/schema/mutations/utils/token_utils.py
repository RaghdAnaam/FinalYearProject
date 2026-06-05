from itsdangerous import URLSafeTimedSerializer
import os

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")

def generate_reset_token(email):
    s = URLSafeTimedSerializer(SECRET_KEY)
    return s.dumps(email, salt="reset-password")

def verify_reset_token(token, max_age=3600):
    s = URLSafeTimedSerializer(SECRET_KEY)
    try:
        return s.loads(token, salt="reset-password", max_age=max_age)
    except Exception:
        return None
