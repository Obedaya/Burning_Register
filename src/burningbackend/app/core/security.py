from passlib.context import CryptContext
import secrets
from hashlib import md5

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a hashed password and a plain password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)



def create_api_key() -> str:
    """Create a random API key."""
    return md5(secrets.token_bytes(32)).hexdigest()