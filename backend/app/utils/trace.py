import random
import string
import time

def generate_trace_id(prefix: str = "BANK") -> str:
    """
    Generates a unique banking audit trace ID in the format BANK-50021
    as specified in HCLTech hackathon specification.
    """
    random_digits = random.randint(10000, 99999)
    return f"{prefix}-{random_digits}"
