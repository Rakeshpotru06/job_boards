from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

SQLALCHEMY_DATABASE_URL = "postgresql://newmek_job:w7z2DXWhK$hlTKg@192.168.2.75/job_board"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:9100340842@localhost:5432/job_boards"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:9100340842@localhost:5432/job_boards"


try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logging.critical(f"Failed to create DB engine: {e}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Error during DB session: {e}")
        raise
    finally:
        db.close()
