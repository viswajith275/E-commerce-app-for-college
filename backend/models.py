from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import List, Optional
from datetime import datetime
import enum
import re

class Base(DeclarativeBase):
    pass

class ItemStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    SOLD = "SOLD"
    WITHDRAWN = "WITHDRAWN"

class BidStatus(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class TransactionStatus(enum.Enum):
    MEET_PENDING = "PENDING"
    COMPLETED = "COMPLETED"

#Base user model
class UsersBase(BaseModel):
    username : str
    email: str
    phone_no: str
    disabled : bool

    model_config = ConfigDict(from_attributes=True)

#user create model
class UserCreate(BaseModel):
    username : str
    email: str
    phone_no: int
    password : str
    confirm_password: str

    @field_validator('username')
    @classmethod
    def username_validation(cls, u: str) -> str:
        if ' ' in u:
            raise ValueError('Username cannot contain spaces')
        return u
    
    @field_validator('email')
    @classmethod
    def email_validation(cls, e: str) -> str:
        if not e.endswith('@gectcr.ac.in'):
            raise ValueError('This is not a student email of GECT')
        return e
    
    @field_validator('phone_no')
    @classmethod
    def phone_no_validation(cls, p: int) -> int:
        if len(str(p)) != 10:
            raise ValueError('This is not a valid phone number!')
        return p
        
    @field_validator('password')
    @classmethod
    def password_constraints(cls, v: str) -> None:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 20:
            raise ValueError('Password must be at most 20 characters long')
        if ' ' in v:
            raise ValueError('Password must not contain a space')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v   
        
    
    @model_validator(mode='after')
    def check_password_match(self) -> 'UserCreate':
        if self.password != self.confirm_password:
            raise ValueError('Confirm password should be same as password!')
        return self



#table structures

#user table schemas
class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    phone_no: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    #relationship with tokens
    tokens: Mapped[List["UserToken"]] = relationship(back_populates='user', cascade='all, delete-orphan')

#User Token data dumping table (have to make a auto cleanup script to clear every week or so)
class UserToken(Base):

    __tablename__ = 'user_tokens'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    access_key: Mapped[Optional[str]] = mapped_column(nullable=True) #change when making access statable object
    refresh_key: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    expires_at: Mapped[datetime] = mapped_column()

    user: Mapped['User'] = relationship(back_populates='tokens')
 
class Item(Base):

    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)

    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    title: Mapped[str] = mapped_column(String(25), nullable=False)
    description: Mapped[str] = mapped_column(String(120))
    price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus), default=ItemStatus.ACTIVE)

    #relationships with


class ItemImage(Base):

    __tablename__ = "item_images"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))

    image_path: Mapped[str] = mapped_column()
    is_primary: Mapped[bool] = mapped_column(default=False)

    #relationship with


class Bid(Base):

    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    bider_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    bid_price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    status: Mapped[BidStatus] = mapped_column(default=BidStatus.PENDING)

    #relationship with


class Transaction(Base):

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    bid_id: Mapped[int] = mapped_column(ForeignKey('bids.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    bider_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    final_price: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    status: Mapped[TransactionStatus] = mapped_column(default=TransactionStatus.MEET_PENDING)

    #relationship with


class Rating(Base):
    pass