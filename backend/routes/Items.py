from fastapi import APIRouter, status, staticfiles, HTTPException, UploadFile, Form, File, Query
from fastapi.staticfiles import StaticFiles
from typing import List, Annotated
from backend.database import SessionDep
from backend.oauth import UserDep
from backend.models import Item, ItemBase, ItemStatus

item_routes = APIRouter()

@item_routes.get('/items', response_model=List[ItemBase])
def Fetch_All_Items(current_user: UserDep, db: SessionDep, skip: int = Query(default=0, ge=0, description="No of items to skip"), limit: int = Query(default=10, ge=1, le=50, description="No of items needed")):

    items = db.query(Item).filter(Item.status == ItemStatus.ACTIVE).order_by(Item.created_at.desc()).offset(skip).limit(limit).all() #have to change the ordering to catagory or something with query variable

    return [{
        'id': item.id,
        'seller_id': item.seller_id,
        'title': item.title,
        'price': item.price,
        'images': [image.image_path for image in item.images]
    } for item in items]

    

@item_routes.post('/items', response_model=ItemBase)
def Createt_Item(current_user: UserDep,
                db: SessionDep,
                title: str = Form(..., min_length=3, max_length=20),
                price: float = Form(...),
                description: str = Form(..., min_length=10, max_length=100),
                images: List[UploadFile] = File(...)):
    pass