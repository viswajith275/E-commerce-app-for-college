from fastapi import APIRouter, status, HTTPException, UploadFile, Form, File, Query
from typing import List
from backend.database import SessionDep
from backend.oauth import UserDep
from backend.utils import validate_image, delete_images, save_image
from backend.models import Item, ItemBase, UniqueItemBase, ItemStatus, ItemImage, BidStatus, Rating, RatingStatus

item_routes = APIRouter(prefix='/items', tags=['Item_Paths'])

@item_routes.get('/feed', response_model=List[ItemBase])
def Fetch_All_Items(current_user: UserDep, db: SessionDep, skip: int = Query(default=0, ge=0, description="No of items to skip"), limit: int = Query(default=10, ge=1, le=50, description="No of items needed")):

    items = db.query(Item).filter(Item.status == ItemStatus.ACTIVE).order_by(Item.created_at.desc()).offset(skip).limit(limit).all() #have to change the ordering to catagory or something with query variable
    
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found!')
    
    result = []

    for item in items:

        primary_photo_path = db.query(ItemImage).filter(ItemImage.is_primary == True, ItemImage.item_id == item.id).first()

        result.append({
        'id': item.id,
        'seller_id': item.seller_id,
        'title': item.title,
        'price': item.price,
        'description': item.description,
        'primary_image': primary_photo_path.image_path,
        'status': item.status,
        'images': [image.image_path for image in item.images if not image.is_primary]
    })


    return result

@item_routes.get('/myitems', response_model=List[ItemBase])
def Fetch_My_Items(current_user: UserDep, db: SessionDep, skip: int = Query(default=0, ge=0, description="No of items to skip"), limit: int = Query(default=10, ge=1, le=50, description="No of items needed")):

    items = db.query(Item).filter(Item.seller_id == current_user.id).order_by(Item.created_at.desc()).offset(skip).limit(limit).all() #have to change the ordering to catagory or something with query variable

    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found!')
    
    result = []

    for item in items:

        primary_photo_path = db.query(ItemImage).filter(ItemImage.item_id == item.id, ItemImage.is_primary == True).first()

        result.append({
        'id': item.id,
        'seller_id': item.seller_id,
        'title': item.title,
        'price': item.price,
        'description': item.description,
        'primary_image': primary_photo_path.image_path,
        'status': item.status,
        'images': [image.image_path for image in item.images if not image.is_primary]
    })
    
    return result
    

@item_routes.get('/{id}', response_model=UniqueItemBase)
def Fetch_One_Item(current_user: UserDep, db: SessionDep, id: int):

    item = db.query(Item).filter(Item.status == ItemStatus.ACTIVE, Item.id == id).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found!')
    
    primary_photo_path = db.query(ItemImage).filter(ItemImage.is_primary == True, ItemImage.item_id == item.id).first()


    return {
        'id': item.id,
        'seller_id': item.seller_id,
        'title': item.title,
        'price': item.price,
        'description':item.description,
        'primary_image': primary_photo_path.image_path,
        'status': item.status,
        'images': [image.image_path for image in item.images if not image.is_primary],
        'bids': [{
            'id': bid.id,
            'bid_price': bid.bid_price,
            'bider_id': bid.bider_id,
            'username': bid.bider.username,
            'rating': bid.bider.rating,
            'status': bid.status
        } for bid in item.bids]
    }


@item_routes.post('/create')
async def Createt_Item(current_user: UserDep,
                db: SessionDep,
                title: str = Form(..., min_length=3, max_length=20),
                price: float = Form(...),
                description: str = Form(..., min_length=10, max_length=100),
                images: List[UploadFile] = File(..., min_length=1, max_length=3)):
    
    pending_rating = db.query(Rating).filter(Rating.rater_id == current_user.id, Rating.status == RatingStatus.PENDING).first()

    if pending_rating:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Complete pending ratings to create a bid!")
    
    
    if price < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The price should be greater than or equal to 0!")

    new_item = Item(seller_id=current_user.id,
                    title=title,
                    description=description,
                    price=price
                    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    for file in images:
        try:
            await validate_image(file=file)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please upload a images within the given constraints!")
    
    for index, file in enumerate(images):
            
            saved_image_path = await save_image(file)
            new_image = ItemImage(item_id=new_item.id,
                                    image_path=saved_image_path,
                                    is_primary= index == 0
                                    )
            db.add(new_image)
            db.commit()

    return {'message': 'Item created successfully!'}

@item_routes.put('/{id}')
async def Update_Item(current_user: UserDep,
                db: SessionDep,
                id: int,
                title: str = Form(..., min_length=3, max_length=20),
                price: float = Form(...),
                description: str = Form(..., min_length=10, max_length=100),
                images: List[UploadFile] | None = File(..., min_length=1, max_length=3)):
    
    pending_rating = db.query(Rating).filter(Rating.rater_id == current_user.id, Rating.status == RatingStatus.PENDING).first()

    if pending_rating:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Complete pending ratings to create a bid!")
    
    
    item = db.query(Item).filter(Item.id == id, Item.seller_id == current_user.id).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found!')
    
    

    item.title = title
    item.price = price
    item.description = description

    if images is not None:

        prev_img_paths = [image.image_path[22::] for image in item.images] #have to change it cannot give a constant no to strip file path

        for path in prev_img_paths:
            await delete_images(path)

        for image in item.images:
            db.delete(image)
        
        db.commit()

        for file in images:
            try:
                await validate_image(file=file)
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please upload a images within the given constraints!")
        
        for index, file in enumerate(images):
                
                saved_image_path = await save_image(file)
                new_image = ItemImage(item_id=item.id,
                                        image_path=saved_image_path,
                                        is_primary= index == 0
                                        )
                db.add(new_image)
                db.commit()
    return {'message': 'Item updated successfully!'}


@item_routes.delete('/{id}')
async def Delete_Item(current_user: UserDep, db: SessionDep, id: int):

    item = db.query(Item).filter(Item.id == id, Item.seller_id == current_user.id).first()
    

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found!')
    
    prev_img_paths = [image.image_path[22::] for image in item.images] #have to change it cannot give a constant no to strip file path

    for path in prev_img_paths:

        await delete_images(path)

    db.delete(item)
    db.commit()

    return {'message': 'successfully deleted the item!'}