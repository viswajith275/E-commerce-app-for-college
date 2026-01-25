from fastapi import APIRouter, status, HTTPException, Query
from typing import List
from backend.database import SessionDep
from backend.oauth import UserDep
from backend.config import BIAS_FACTOR
from backend.models import Rating, RatingBase, RatingStatus, RatingCreate, TransactionStatus


rating_routes = APIRouter(prefix='/ratings', tags=['Rating_Paths'])

@rating_routes.get('/myratings', response_model=List[RatingBase])
def Fetch_My_Ratings(current_user: UserDep, db: SessionDep):

    ratings = db.query(Rating).filter(Rating.rater_id == current_user.id).all()

    if not ratings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ratings found!")
    
    result = []
    for rating in ratings:
        result.append({
            'id': rating.id,
            'rated_username': rating.rated_user.username,
            'rated_score': rating.score,
            'rating_status': rating.status
        })

    return result

@rating_routes.get('/mypending', response_model=List[RatingBase])
def Fetch_My_Pending_Rating(current_user: UserDep, db: SessionDep):
    ratings = db.query(Rating).filter(Rating.rater_id == current_user.id, Rating.status == RatingStatus.PENDING).all()

    if not ratings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pending ratings found!")
    
    result = []
    for rating in ratings:
        result.append({
            'id': rating.id,
            'rated_username': rating.rated_user.username,
            'rated_score': rating.score,
            'rating_status': rating.status
        })

    return result

@rating_routes.post('/pending')
def Update_Rating(current_user: UserDep, db: SessionDep, rating_data: RatingCreate):

    rating = db.query(Rating).filter(Rating.id == rating_data.rating_id, Rating.rater_id == current_user.id, Rating.status == RatingStatus.PENDING).first()

    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ratings found!")
    
    rating.score = rating_data.rated_score
    rating.status = RatingStatus.RATED
    rating.transaction.status = TransactionStatus.COMPLETED

    if rating_data.rated_score < 5:
        weight = 1 + ((5 - rating_data.rated_score) * (BIAS_FACTOR - 1))
    else:
        weight = 1

    current_user.rating_count += weight
    current_user.total_rating += (rating_data.rated_score * weight)


    db.commit()

    current_user.rating = round(current_user.total_rating / current_user.rating_count, 2) 

    db.commit()

    return {'message': "Rating updated successfully!"}

    