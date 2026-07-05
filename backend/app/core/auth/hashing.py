import bcrypt

def hash_password(password: str) -> str:
    """
    Encrypts a plain text password into a secure hash using bcrypt directly.
    """
    # Convert password to bytes and generate a salt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    
    # Hash and return as a decoded string
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a plain text password with a stored bcrypt hash.
    Returns True if they match, and False otherwise.
    """
    # Encode both inputs to bytes and verify
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)
