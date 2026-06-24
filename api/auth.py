import jwt, bcrypt, os
from datetime import datetime, timedelta

SECRET = os.getenv('SECRET_KEY', 'sarab_secret')

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def create_token(user_id):
    return jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=30)}, SECRET)
