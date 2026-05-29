import jwt
from datetime import datetime, timedelta, timezone
import uuid

from settings.config import *

class TokenService():
    def create_access_token(self, user_id):
        token_data = {"type":"access",
                      "user_id":user_id,
                      "exp":datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)}
        
        token = jwt.encode(token_data, ACCESS_KEY, "HS256")
        return token
    
    def create_refresh_token(self, user_id):
        jti = uuid.uuid4().hex#jti = token id

        token_data = {"type":"refresh",
                      "user_id":user_id,
                      "exp":datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_DAYS),
                      "jti":jti}
        
        token = jwt.encode(token_data, REFRESH_KEY, "HS256")
        return token, jti
    
    def decrypt_refresh_token(self, token):
        if type(token) == str:
            token = token.encode()
            
        token_data = jwt.decode(token, REFRESH_KEY, "HS256")
        
        return token_data

    def decrypt_access_token(self, token):
        if type(token) == str:
            token = token.encode()
            
        token_data = jwt.decode(token, ACCESS_KEY, "HS256")
        
        return token_data
