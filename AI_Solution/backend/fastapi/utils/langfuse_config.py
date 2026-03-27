import os
from langfuse import Langfuse
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")
print(f"Langfuse configured: {bool(LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY)}")
print(f"Langfuse host: {LANGFUSE_HOST}")
langfuse_client = None

def init_langfuse():
    global langfuse_client
    
    if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
        try:
            langfuse_client = Langfuse(
                public_key=LANGFUSE_PUBLIC_KEY,
                secret_key=LANGFUSE_SECRET_KEY,
                host=LANGFUSE_HOST
            )
            print("Langfuse initialized successfully")
            return langfuse_client
        except Exception as e:
            print(f"Langfuse initialization failed: {e}")
            return None
    else:
        print("Langfuse keys not found - tracking disabled")
        return None

def get_langfuse_client():
    global langfuse_client
    if langfuse_client is None:
        langfuse_client = init_langfuse()
    return langfuse_client

init_langfuse()