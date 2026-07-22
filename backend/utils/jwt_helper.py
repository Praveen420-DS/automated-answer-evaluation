import jwt
from config import Config
def create_token(data): return jwt.encode(data,Config.SECRET_KEY,algorithm='HS256')
def decode_token(token):
 try: return jwt.decode(token,Config.SECRET_KEY,algorithms=['HS256'])
 except jwt.PyJWTError: return None
