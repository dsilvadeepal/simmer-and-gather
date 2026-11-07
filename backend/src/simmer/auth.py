import jwt
from cryptography.fernet import Fernet

class Authenticator:
    def __init__(self, key, allowed_owner, issuer, audience, algorithms=None):
        self.key,self.allowed,self.issuer,self.audience=key,allowed_owner,issuer,audience
        self.algorithms=algorithms or ['HS256']
    def require_owner(self, session_token):
        try:
            claims=jwt.decode(session_token,self.key,algorithms=self.algorithms,audience=self.audience,issuer=self.issuer,options={'require':['exp','sub','iss','aud']})
            if not self.allowed or claims['sub']!=self.allowed: raise ValueError()
            return claims['sub']
        except (jwt.PyJWTError,ValueError) as e: raise ValueError('Login required') from e

def encrypt_secret(value,key): return Fernet(key.encode()).encrypt(value.encode()).decode()
def decrypt_secret(value,key): return Fernet(key.encode()).decrypt(value.encode()).decode()
