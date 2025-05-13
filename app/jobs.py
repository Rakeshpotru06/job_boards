from app.db.session import SessionLocal
import time

from app.services.user_service import set_cache_data

# to start the scheduler
def refresh_cache():
    db = SessionLocal()
    try:
        users = set_cache_data(db,'users_data')
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ Refreshed {len(users)} users")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()
