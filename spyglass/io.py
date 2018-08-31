import yaml
import pyperclip

from .encryption import encrypt, decrypt


def copy_to_clipboard(stuff):
    """Copy stuff to clipboard.
    """
    pyperclip.copy(stuff)


# ------- Handle Encryption file ----------

def read_encryption_key(key_path):
    """Read encryption key from disk."""
    with open(key_path, "rb") as f:
        key = f.read()
    return key


def write_encryption_key(key, key_path):
    """Write key to keyfile."""
    with open(key_path, "wb") as f:
        f.write(key)


# ------- Handle YAML ----------------------

def read_yaml(yml):
    """Parse yaml data. Return python dictionary."""
    data = yaml.load(yml)
    if data == b'':
        data = {}
    return data

def to_yaml(data):
    """Python dictionary to YAML."""
    return yaml.dump(data, default_flow_style=False)

# ------- Handle password file ------------


def read_password_file(password_file, encryption_key):
    """Open password file, decrypt it, 
    """
    # Read file.
    with open(password_file, "rb") as f:
        encrypted_data = f.read()
        # Decrypt file
        yml = decrypt(encrypted_data, encryption_key)
        # Parse yaml
        data = read_yaml(yml)
    return data


def write_password_file(data, encryption_key, password_file): 
    """Write data to file.
    """
    # Convert python data to yaml.
    yml = to_yaml(data)

    # Encrypt yaml.
    encrypted_yml = encrypt(yml, encryption_key)

    # Write to file.
    with open(password_file, "wb") as f:
        f.write(encrypted_yml)
