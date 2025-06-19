from config.database import SessionLocal
from models.document_type import DocumentType


def get_all_document_types():
    db = SessionLocal()
    try:
        return db.query(DocumentType).all()
    finally:
        db.close()


def get_document_type_by_name(type_name: str):
    db = SessionLocal()
    try:
        return db.query(DocumentType).filter(DocumentType.type_name == type_name).first()
    finally:
        db.close()

