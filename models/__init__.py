from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./production.db", echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from .user import User
from .warehouse import Warehouse
from .material import Material
from .stock_balance import StockBalance
from .transfer_route import TransferRoute
from .transfer_order import TransferOrder
from .shipment import Shipment
from .receipt import Receipt
from .document_type import DocumentType
from .transfer_loss import TransferLoss

def init_db():
    Base.metadata.create_all(bind=engine)