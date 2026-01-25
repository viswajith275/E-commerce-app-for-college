from sqlalchemy import String, ForeignKey, Enum, or_
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import List, Optional
from datetime import datetime
import enum
import re
from backend.config import MAX_IMAGE_SIZE

ALLOWED_TYPES = ["image/jpeg", "image/png"]

class Base(DeclarativeBase):
    pass

class ItemStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    SOLD = "SOLD"
    
    
class BidStatus(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class TransactionStatus(enum.Enum):
    MEET_PENDING = "MEET_PENDING"
    COMPLETED = "COMPLETED"

class RatingStatus(enum.Enum):
    PENDING = "PENDING"
    RATED = "RATED"

class ImageValidatorSchema(BaseModel):

    filename: str
    content_type: str
    file_size: int

    @field_validator('content_type')
    @classmethod
    def validate_file_type(cls, v):
        if v not in ALLOWED_TYPES:
            raise ValueError(f"File type '{v}' not allowed. Must be JPEG or PNG.")
        return v

    @field_validator('file_size')
    @classmethod
    def validate_size(cls, v):
        if v > MAX_IMAGE_SIZE:
            raise ValueError(f"File too large. Max size is {MAX_IMAGE_SIZE / 1024 / 1024}MB")
        return v

#Base user model
class UsersBase(BaseModel):
    username : str
    email: str
    phone_no: str
    rating: float
    disabled : bool

    model_config = ConfigDict(from_attributes=True)

#user create model
class UserCreate(BaseModel):
    username : str
    email: str
    phone_no: str
    password : str
    confirm_password: str

    @field_validator('username')
    @classmethod
    def username_validation(cls, u: str) -> str:
        if len(u) < 3:
            raise ValueError('Username cannot be smaller than 3 characters!')

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
    def phone_no_validation(cls, p: str) -> str:
        try:
            p = str(int(p))

            if len(p) != 10:
                raise ValueError('This is not a valid phone number!')
            
            return p
        except:
            raise ValueError('This is not a valid phone number!')

        
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
    
class RatingBase(BaseModel):
    id: int
    rated_username: str
    rated_score: int
    rating_status: RatingStatus

class RatingCreate(BaseModel):
    rating_id: int
    rated_score: int

    @field_validator('rated_score')
    @classmethod
    def rated_score_validator(cls, s: int):
        if s > 5 or s < 0:
            raise ValueError("The score should be between 1 and 5")
        return s

class TransactionBase(BaseModel):
    seller_username: str
    buyer_username: str
    final_price: float
    status: TransactionStatus

class TransactionCreate(BaseModel):
    item_id: int
    bid_id: int

class TransactionContact(BaseModel):
    username: str
    email: str
    phone_no: str
    
class MyBidBase(BaseModel):
    id: int
    bid_price: float
    username: str
    rating: float
    status: BidStatus
    
class BidBase(MyBidBase):
    bider_id: int


class BidCreate(BaseModel):
    item_id: int
    bid_price: float

    @field_validator('bid_price')
    @classmethod
    def bid_price_validator(cls, p: float) -> float:
        if p < 0:
            raise ValueError("The price cannot be less than 0!")
        return p

class BidUpdate(BaseModel):
    bid_price: float

    @field_validator('bid_price')
    @classmethod
    def bid_price_validator(cls, p: float) -> float:
        if p < 0:
            raise ValueError("The price cannot be less than 0!")
        return p

class ItemBase(BaseModel):
    id: int
    seller_id: int
    title: str
    description: str
    price: float
    primary_image: str
    images: List[str]
    status: ItemStatus

class UniqueItemBase(ItemBase):
    bids: List[BidBase]


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
    rating_count: Mapped[int] = mapped_column(default=0)
    total_rating: Mapped[int] = mapped_column(default=0)
    rating: Mapped[float] = mapped_column(default=2.5)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    #relationship with tokens
    tokens: Mapped[List["UserToken"]] = relationship(back_populates='user', cascade='all, delete-orphan')
    listed_items: Mapped[List["Item"]] = relationship(back_populates="seller", cascade="all, delete-orphan")
    all_bids: Mapped[List["Bid"]] = relationship(back_populates='bider', cascade='all, delete-orphan')
    selled_item_transactions: Mapped[List[Transaction]] = relationship(foreign_keys="[Transaction.seller_id]", back_populates='seller')
    buyed_item_transactions: Mapped[List[Transaction]] = relationship(foreign_keys="[Transaction.bider_id]", back_populates='bider')


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

    images: Mapped[List["ItemImage"]] = relationship(back_populates='item', cascade='all, delete-orphan')
    seller: Mapped['User'] = relationship(back_populates='listed_items')
    bids: Mapped[List['Bid']] = relationship(back_populates='item', cascade='all, delete-orphan')
    transaction: Mapped["Transaction"] = relationship(back_populates='item', cascade='all, delete-orphan')

class ItemImage(Base):

    __tablename__ = "item_images"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))

    image_path: Mapped[str] = mapped_column()
    is_primary: Mapped[bool] = mapped_column(default=False)

    #relationship with

    item: Mapped["Item"] = relationship(back_populates='images')

class Bid(Base):

    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(primary_key=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    bider_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    bid_price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    status: Mapped[BidStatus] = mapped_column(default=BidStatus.PENDING)

    #relationship with

    item: Mapped['Item'] = relationship(back_populates='bids')
    bider: Mapped['User'] = relationship(back_populates='all_bids')

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

    item: Mapped['Item'] = relationship(back_populates='transaction')
    ratings: Mapped[List["Rating"]] = relationship(back_populates='transaction', cascade='all, delete-orphan')
    seller: Mapped["User"] = relationship(foreign_keys=[seller_id], back_populates='selled_item_transactions')
    bider: Mapped["User"] = relationship(foreign_keys=[bider_id], back_populates='buyed_item_transactions')



class Rating(Base):
    
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True)

    trasaction_id: Mapped[int] = mapped_column(ForeignKey('transactions.id'))
    rater_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    rated_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    score: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    status: Mapped[RatingStatus] = mapped_column(default=RatingStatus.PENDING)

    #relationship with

    transaction: Mapped["Transaction"] = relationship(back_populates='ratings')
    rater_user: Mapped["User"] = relationship(foreign_keys=[rater_id])
    rated_user: Mapped["User"] = relationship(foreign_keys=[rated_id])

