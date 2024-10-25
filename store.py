from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from pydantic import BaseModel
from typing import List

app = FastAPI()


URL = "sqlite:///./test.db"
engine = create_engine(URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, index= True)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, index= True)
    price = Column(Integer)

class Basket(Base):
    __tablename__ = 'baskets'
    id = Column(Integer, primary_key = True, index= True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship('User', back_populates= 'baskets')
    products = relationship("Product", secondary="cart_items")
    
class Basket_item(Base):
    __tablename__ = 'basket_items'
    basket_id = Column(Integer, ForeignKey('baskets.id'), primary_key= True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key= True)

# shema
class ProductBase(BaseModel):
    name: str
    price: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    products: List[Product] = []

# pointy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post('/products/', response_model= Product)
def create_product(product: ProductCreate, db):# дописать надо добавление в db
    return product

# @app.get('/products'):
    

