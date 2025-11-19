from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create the engine (The connection to the file)
# connect_args is needed only for SQLite to allow multiple threads
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
# Each instance of this class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session in other parts of the app
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()