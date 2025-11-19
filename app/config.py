import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "GripInvest+3"
    PROJECT_VERSION: str = "1.0.0"
    
    # This creates a simple file-based DB named 'gripinvest.db' in the main folder
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./gripinvest.db")

settings = Settings()