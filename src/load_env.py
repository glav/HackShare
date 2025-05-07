from dotenv import load_dotenv
import os

def load_env():
    """Locate and load .env file, returning load status."""
    dotenv_path = None
    for path in [".env", "../.env"]:
        if os.path.exists(path):
            dotenv_path = path
            break
    env_loaded = load_dotenv(dotenv_path=dotenv_path, override=True)
    print(f"Env variables loaded: {env_loaded}")
    return env_loaded
