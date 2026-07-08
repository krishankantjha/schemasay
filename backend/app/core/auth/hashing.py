import bcrypt

def hash_password(password: str) -> str:
    """
    Encrypts a plain text password into a secure hash using bcrypt directly.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a plain text password with a stored bcrypt hash.
    Returns True if they match, and False otherwise.
    """
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)
