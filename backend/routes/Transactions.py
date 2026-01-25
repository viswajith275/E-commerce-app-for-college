from fastapi import APIRouter, status, HTTPException, Query
from typing import List
from backend.database import SessionDep
from backend.oauth import UserDep
from backend.models import Transaction, TransactionStatus, TransactionBase, TransactionCreate, Item, Bid, ItemStatus, BidStatus, Rating, TransactionContact

transaction_routes = APIRouter(prefix='/transactions', tags=["Transaction_Paths"])

@transaction_routes.get('/mytransactions', response_model=List[TransactionBase])
def Fetch_All_Transactions(current_user: UserDep, db: SessionDep):

    transactions = current_user.selled_item_transactions + current_user.buyed_item_transactions

    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found!")
    
    result = []

    for transaction in transactions:
        result.append({
            "seller_username": transaction.seller.username,
            "buyer_username": transaction.bider.username,
            "final_price": transaction.final_price,
            "status": transaction.status
        })

    return result


@transaction_routes.post('/confirm', response_model=TransactionContact)
def Create_Transaction(current_user: UserDep, db: SessionDep, transaction_data: TransactionCreate):
    
    bid = db.query(Bid).join(Item).filter(Item.id == transaction_data.item_id, Item.status == ItemStatus.ACTIVE, Item.seller_id == current_user.id).filter(Bid.id == transaction_data.bid_id).first()

    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The item not found or already been sold!")
    try:
        bid.item.status = ItemStatus.SOLD

        bid.status = BidStatus.ACCEPTED

        rejected_bids = db.query(Bid).filter(Bid.item_id == bid.item_id, Bid.id != bid.id).all()

        for bid in rejected_bids:

            bid.status = BidStatus.REJECTED
        
        new_transaction = Transaction(item_id = bid.item_id, bid_id = bid.id, seller_id = bid.item.seller_id, bider_id = bid.bider_id, final_price = bid.bid_price, status = TransactionStatus.MEET_PENDING)

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        seller_rating = Rating(transaction_id=new_transaction.id, rater_id=new_transaction.seller_id, rated_id=new_transaction.bider_id)
        bider_rating = Rating(transaction_id=new_transaction.id, rater_id=new_transaction.bider_id, rated_id=new_transaction.seller_id)

        db.add(seller_rating)
        db.add(bider_rating)
        db.commit()

        return {
            'username': new_transaction.bider.username,
            'email': new_transaction.bider.email,
            'phone_no': new_transaction.bider.phone_no
        }
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transction failed!")
    