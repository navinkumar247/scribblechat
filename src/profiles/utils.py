
from uuid import uuid4

def get_unique_code():
    return str(uuid4())[:10]