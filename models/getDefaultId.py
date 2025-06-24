import random
import string

def generate_custom_id(prefix: str) -> str:
    """Generates a custom ID with a prefix and 10 random digits."""
    random_digits = ''.join(random.choices(string.digits, k=10))
    return f"{prefix}:{random_digits}"