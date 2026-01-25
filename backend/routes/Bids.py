from fastapi import APIRouter, status, HTTPException, Query
from typing import List
from backend.database import SessionDep
from backend.oauth import UserDep
from backend.models import Bid, MyBidBase, BidStatus, BidCreate, Item, ItemStatus, BidUpdate

bid_routes = APIRouter(prefix='/bids', tags=['Bid_Paths'])

@bid_routes.get('/mybids', response_model=List[MyBidBase])
def Fetch_My_Bids(current_user: UserDep,):

    bids = current_user.all_bids

    if not bids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bids found!")
    
    result = []

    for bid in bids:
        result.append({
            'id': bid.id,
            
            'bid_price': bid.bid_price,
            'username': bid.bider.username,
            'rating': bid.bider.rating,
            'status': bid.status
        })

    return result


@bid_routes.post("/create")
def Create_Bid(current_user: UserDep, db: SessionDep, bid_data: BidCreate):
    
    item = db.query(Item).filter(Item.id == bid_data.item_id, Item.status == ItemStatus.ACTIVE).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item sold or does not exist!")
    
    if item.seller_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot place bid on your own item!")
    
    exist = db.query(Bid).filter(Bid.bider_id == current_user.id, Bid.item_id == bid_data.item_id, Bid.status == BidStatus.PENDING).first()

    if exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You cant place multiple bids on the same item!")
    
    new_bid = Bid(bider_id=current_user.id, item_id=item.id, bid_price=bid_data.bid_price)

    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)

    return {'message': "Bid created successfully!"}

@bid_routes.put('/{id}')
def Update_Bid(current_user: UserDep, db: SessionDep, id: int, bid_data: BidUpdate):

    bid = db.query(Bid).filter(Bid.id == id, Bid.bider_id == current_user.id, Bid.status == BidStatus.PENDING).first()

    if bid is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found!")
    
    bid.bid_price = bid_data.bid_price

    db.commit()

    return {'message': "Bid Updated successfully!"}


@bid_routes.delete('/{id}')
def Delete_Bid(current_user: UserDep, db: SessionDep, id: int):

    bid = db.query(Bid).filter(Bid.id == id, Bid.bider_id == current_user.id, Bid.status == BidStatus.PENDING).first()

    if bid is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid accepted or not found!")
    
    db.delete(bid)
    db.commit()

    return {'message': "Bid deleted successfully!"}