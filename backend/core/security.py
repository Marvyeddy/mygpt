# Functions for hashing and verifying passwords
from argon2 import PasswordHasher, exceptions

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plain password."""
    return password_hasher.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """Verify a plain password against the given hashed password."""
    try:
        return password_hasher.verify(hashed_password, password)
    except exceptions.VerifyMismatchError:
        return False
