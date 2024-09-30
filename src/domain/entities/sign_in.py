from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
class SignIn(BaseModel):
    """
    SignIn model for user sign in.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    email: str
    password: str

class Token(BaseModel):
    """
    Token model for user access token.
    """
    access_token: str
    token_type: str