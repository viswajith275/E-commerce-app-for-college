from fastapi import APIRouter, status, staticfiles, HTTPException, UploadFile, Form, File, Query
from fastapi.staticfiles import StaticFiles
from typing import List, Annotated
from backend.database import SessionDep
from backend.oauth import UserDep
from backend.models import Item, ItemBase, UniqueItemBase, ItemStatus, ItemImage

item_routes = APIRouter(prefix='/items', tags=['Item_Paths'])

@item_routes.get('/feed', response_model=List[ItemBase])
def Fetch_All_Items(current_user: UserDep, db: SessionDep, skip: int = Query(default=0, ge=0, description="No of items to skip"), limit: int = Query(default=10, ge=1, le=50, description="No of items needed")):

    items = db.query(Item).filter(Item.status == ItemStatus.ACTIVE).order_by(Item.created_at.desc()).offset(skip).limit(limit).all() #have to change the ordering to catagory or something with query variable

    result = []

    for item in items:

        primary_photo_path = db.query(ItemImage).filter(ItemImage.is_primary == True, ItemImage.item_id == item.id).first()

        result.append({
        'id': item.id,
        'seller_id': item.seller_id,
        'title': item.title,
        'price': item.price,
        'primary_image': primary_photo_path,
        'images': [image.image_path for image in item.images if not image.is_primary]
    })


    return result

@item_routes.get('/{id}', response_model=UniqueItemBase)
def Fetch_One_Item(current_user: UserDep, db: SessionDep, id: int):

    item = db.query(Item).filter(Item.status == ItemStatus.ACTIVE, Item.id == id).first()
    primary_photo_path = db.query(ItemImage).filter(ItemImage.is_primary == True, ItemImage.item_id == item.id).first()


    return {
        'id': item.id,
        'seller_id': item.seller_id,
        'title': item.title,
        'price': item.price,
        'primary_image': primary_photo_path,
        'images': [image.image_path for image in item.images if not image.is_primary],
        'bids': [{
            'id': bid.id,
            'bid_price': bid.bid_price,
            'username': bid.bider.username,
            'rating': bid.bider.rating
        } for bid in item.bids]
    }
    

@item_routes.post('/create', response_model=UniqueItemBase)
def Createt_Item(current_user: UserDep,
                db: SessionDep,
                title: str = Form(..., min_length=3, max_length=20),
                price: float = Form(...),
                description: str = Form(..., min_length=10, max_length=100),
                images: List[UploadFile] = File(...)):
    pass