import os
import shutil
import click
from pathlib import Path

# Imports from spyglass
from . import passwords
from . import encryption
from . import io

SPYGLASS_PATH = os.path.join(str(Path.home()), ".spyglass")
PW_FILE = "password.txt"
KEY_FILE = ".key.txt"


@click.group()
def spyglass():
    """Spyglass is a simple and secure tool for managing your passwords in Python."""


@spyglass.command("init", help="Initialize the spyglass password repository.")
def init():
    """Initialize a spyglass password database.
    """
    # Create Spyglass directory
    path = os.path.join(SPYGLASS_PATH)
    if not os.path.exists(path):
        os.makedirs(path)

    # Write encryption key to disk.
    key = encryption.get_key()

    # Create password file
    password_path = os.path.join(SPYGLASS_PATH, PW_FILE)
    if not os.path.exists(password_path):
        io.write_password_file(b'', key, password_path)

    # Create a key file.
    key_path = os.path.join(SPYGLASS_PATH, KEY_FILE)
    if not os.path.exists(key_path):
        io.write_encryption_key(key, key_path)


@spyglass.command("add", help="Add a password to the database.")
@click.argument("key")
@click.argument("username")
@click.option("-p", "--password", default=None, help="User defined password.")
@click.option("-l", "--length", default=12, help="Password length.")
@click.option("-c", "--characters", default=0, help="Password characters. 0: lowercase chars, 1: +uppercase, 2: +numeric, 3: +special.")
def add(key, username, password, length, characters):
    """Add a password to the database.
    """
    # Path to password file.
    password_path = os.path.join(SPYGLASS_PATH, PW_FILE)
    key_path = os.path.join(SPYGLASS_PATH, KEY_FILE)

    # Get encryption_key
    encryption_key = io.read_encryption_key(key_path)

    # Read encrypted password data.
    data = io.read_password_file(password_path, encryption_key)

    if key in data:
        print()
        print(f'"{key}" is already used in spyglass. Either remove "{key}" or use a different key.')
        print()
        return None

    if password is None:
        # Password types.
        alphabet_options = {
            0: {"alpha": True, "capital": False, "numeric": False, "special": False},
            1: {"alpha": True, "capital": True, "numeric": False, "special": False},
            2: {"alpha": True, "capital": True, "numeric": True, "special": False},
            3: {"alpha": True, "capital": True, "numeric": True, "special": True},
        }

        # Get data you care about
        password = passwords.generate_password(
            length,
            **alphabet_options[characters]
        )

    # Evaluate strength of password.
    results = passwords.calculate_strength(password, full_report=True)
    passwords.print_score_results(results)

    # Add new item
    data[key] = {
        'username': username,
        'password': password
    }

    # Write encrypted file.
    io.write_password_file(data, encryption_key, password_path)

    print("Password successfully added!")
    print()

@spyglass.command("rm", help="Remove field in password database.")
@click.argument("key")
def rm(key):
    """Remove password from database.
    """
    # Path to password file.
    password_path = os.path.join(SPYGLASS_PATH, PW_FILE)
    key_path = os.path.join(SPYGLASS_PATH, KEY_FILE)

    # Get encryption_key
    encryption_key = io.read_encryption_key(key_path)

    # Read encrypted password data.
    data = io.read_password_file(password_path, encryption_key)

    # Remove element
    del data[key]

    # Write encrypted file.
    io.write_password_file(data, encryption_key, password_path)


@spyglass.command("get", help="Name/key for password")
@click.argument("key")
@click.option("--show", is_flag=True, help="Shows password as plain text if given.")
def get(key, show):
    """Get password copied to clipboard."""
    # Path to password file.
    password_path = os.path.join(SPYGLASS_PATH, PW_FILE)
    key_path = os.path.join(SPYGLASS_PATH, KEY_FILE)

    # Get encryption_key
    encryption_key = io.read_encryption_key(key_path)

    # Read encrypted password data.
    data = io.read_password_file(password_path, encryption_key)

    # Get data you care about
    item = data[key]
    username = item["username"]
    password = item["password"]

    # Print username to console.
    print()
    print(f"Username: {username}")
    print("Password copied to clipboard!")
    if show:
        print(f"Password: {password}")
    print()
    # Copy to clipboard.
    io.copy_to_clipboard(password)


@spyglass.command("ls", help="List command")
@click.option("-u", "--username", is_flag=True, help="Show usename.")
@click.option("-p", "--password", is_flag=True, help="Show password.")
def ls(username, password):
    """List the password keys."""
    # Path to password file.
    password_path = os.path.join(SPYGLASS_PATH, PW_FILE)
    key_path = os.path.join(SPYGLASS_PATH, KEY_FILE)

    # Get encryption_key
    encryption_key = io.read_encryption_key(key_path)

    # Read encrypted password data.
    data = io.read_password_file(password_path, encryption_key)

    print()
    print("Spyglass keys:")
    # Print keys.
    for key in data:
        print(f"  - {key}")
        
        if username:
            user = data[key]["username"]
            print(f"    - username: {user}")

        if password: 
            passwd = data[key]["password"]
            print(f"    - password: {passwd}")
    print()


@spyglass.command("score", help="Score a password")
@click.argument("password")
@click.option("-a", "-all", is_flag=True, help="Report all statistics.")
def score(password, all):
    """Score a password
    """
    results = passwords.calculate_strength(password, full_report=True)
    passwords.print_score_results(results, full_report=all)