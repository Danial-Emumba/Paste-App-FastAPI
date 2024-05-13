from app.db.setup import SessionLocal
from app.storage.s3 import delete_from_s3
from app.db.repository import delete_expired_pastes

def cleanup_expired_pastes():
    db = SessionLocal()
    try:
        print('Cleaning up expired pastes...')
        expired_pastes = delete_expired_pastes(db)
        if expired_pastes is not None:
            for paste in expired_pastes:
                delete_from_s3(paste.shortlink)
            db.commit()
            print("Expired pastes cleaned up successfully.")
        else:
            return
    except Exception as e:
        db.rollback()
        print(f"Failed to clean up expired pastes: {e}")
        raise e
    finally:
        db.close()

