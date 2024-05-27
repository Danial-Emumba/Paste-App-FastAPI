from bcrypt import checkpw, gensalt, hashpw

def generate_password_hash(password: str) -> str:
    """
    Generates a secure password hash using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password_hash(hashed_password: str, password: str) -> bool:
    """
    Checks if the provided password matches the stored hashed password.

    Args:
        hashed_password (str): The hashed password stored in the database.
        password (str): The plain text password to check.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
