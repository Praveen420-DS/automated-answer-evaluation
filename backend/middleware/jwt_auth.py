from functools import wraps
from flask import request
from utils.jwt_helper import decode_token
def jwt_required(fn):
 @wraps(fn)
 def wrapped(*args,**kwargs):
  token=request.headers.get('Authorization','').replace('Bearer ','')
  request.user=decode_token(token)
  return fn(*args,**kwargs)
 return wrapped
