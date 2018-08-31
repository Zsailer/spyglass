from cryptography.fernet import Fernet

def get_key():
    """Get an encryption key."""
    key = Fernet.generate_key()
    return key

def encrypt(data, key):
    """Encrypt password data."""
    # Initialize Decrypter
    cipher = Fernet(key)
    # Encode data as binary.
    data = data.encode()
    # Encrypty data.
    binary = cipher.encrypt(data)
    return binary


def decrypt(data, key):
    """Decrypt password data."""
    # Initialize Decrypter
    cipher = Fernet(key)
    # Decrypt data.
    text = cipher.decrypt(data)
    # Decode
    text = text.decode('utf-8')
    return text
