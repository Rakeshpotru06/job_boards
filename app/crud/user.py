from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.logger import logger

def get_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Database error in get_users: {e}")
        raise

def get_users_with_count(db: Session, skip: int = 0, limit: int = 100):
    total = db.query(User).count()
    users = db.query(User).offset(skip).limit(limit).all()
    return users, total