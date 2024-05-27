from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///crypto_trading_app.db"

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    symbol = Column(String)
    amount = Column(Float)
    price = Column(Float)
    leverage = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    type = Column(String)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_order(symbol, amount, price, leverage, stop_loss, take_profit, order_type):
    order = Order(
        symbol=symbol,
        amount=amount,
        price=price,
        leverage=leverage,
        stop_loss=stop_loss,
        take_profit=take_profit,
        type=order_type
    )
    session.add(order)
    session.commit()

def get_orders():
    return session.query(Order).all()

