from sqlalchemy.orm import Session
from app.db.models.jobs import Jobs
from app.core.logger import logger

def get_jobs(db: Session, skip: int = 0):
    try:
        return db.query(Jobs).order_by(Jobs.id.asc()).offset(skip).all()
    except Exception as e:
        logger.error(f"Database error in get_jobs: {e}")
        raise

