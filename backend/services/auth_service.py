from utils.jwt_helper import create_token
def authenticate(email,password):
    if not email or not password: return None
    return {'user':{'email':email,'role':'student'},'token':create_token({'email':email,'role':'student'})}
def create_user(data): return {'email':data.get('email'),'role':data.get('role','student')}
