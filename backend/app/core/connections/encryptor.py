from cryptography.fernet import Fernet
from app.config import settings

# Initialize the encryption key from settings (.env)
# The key is expected to be a 32-byte, url-safe, base64-encoded string
try:
    fernet = Fernet(settings.ENCRYPTION_KEY.encode('utf-8'))
except Exception as e:
    raise RuntimeError(
        f"Failed to initialize encryption engine. Ensure ENCRYPTION_KEY is a valid base64 key: {str(e)}"
    )

def encrypt_password(password: str) -> str:
    """
    Encrypts a plain-text database password into a secure, encrypted Fernet string.
    
    Args:
        password: The plain-text password to encrypt.
        
    Returns:
        A base64-encoded encrypted string, or an empty string if input is empty.
    """
    if not password:
        return ""
    password_bytes = password.encode('utf-8')
    encrypted_bytes = fernet.encrypt(password_bytes)
    return encrypted_bytes.decode('utf-8')

def decrypt_password(encrypted_password: str) -> str:
    """
    Decrypts an encrypted Fernet password string back into plain-text.
    
    Args:
        encrypted_password: The base64-encoded Fernet encrypted string to decrypt.
        
    Returns:
        The decrypted plain-text password, or an empty string if input is empty.
    """
    if not encrypted_password:
        return ""
    encrypted_bytes = encrypted_password.encode('utf-8')
    decrypted_bytes = fernet.decrypt(encrypted_bytes)
    return decrypted_bytes.decode('utf-8')
