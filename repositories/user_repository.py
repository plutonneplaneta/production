from config.database import SessionLocal
from models.user import User
from sqlalchemy import text

def get_user_by_username(username: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()

def get_all_users():
    db = SessionLocal()
    try: 
        return db.query(User).all()
    except Exception as e:
        print(f"Ошибка при получении пользователей:{e}")
    finally:
        db.close()
def create_user(username: str, password: str, full_name: str, role: str):
    db = SessionLocal()
    try:
        new_user = User(
            username=username,
            password=password,
            full_name=full_name,
            role=role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        '''if role == 'admin':
            db.execute(text("GRANT ALL PRIVILEGES ON users TO :username"), {"username": username})'''
        return new_user
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании пользователя: {e}")
        raise e
    finally:
        db.close()

def delete_user_by_username(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()

        if user:
            db.delete(user)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка при удалении пользователя: {e}")
        raise e
    finally:
        db.close()

from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import engine 

def update_user_by_username(username, password=None, role=None, is_active=None):
    """
    Обновляет данные пользователя по username.
    """
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.username == username)).first()
        if not user:
            raise ValueError(f"Пользователь '{username}' не найден")

        if password is not None:
            user.password = password
        if role is not None:
            user.role = role
        if is_active is not None and hasattr(user, "is_active"):
            user.is_active = is_active

        session.commit()
        return user