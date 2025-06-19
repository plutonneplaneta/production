from config.database import SessionLocal

def get_db_session():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()