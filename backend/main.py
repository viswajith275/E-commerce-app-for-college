from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from .routes.Login import login_routes
from .routes.Items import item_routes
from .routes.Bids import bid_routes
from .routes.Transactions import transaction_routes
from .routes.Ratings import rating_routes
from backend.database import create_db_and_tables
from backend.config import UPLOAD_DIRECTORY

app = FastAPI()


#starting the server and creating tables
@app.on_event('startup')
def startup():
    create_db_and_tables()

abs_path = os.path.dirname(os.path.abspath(__file__))
new_path = os.path.join(abs_path, UPLOAD_DIRECTORY)
os.makedirs(new_path, exist_ok=True)

app.mount(path='/static', app=StaticFiles(directory='static'), name="static")

origins = ["http://localhost:5173"]

#Added the local react server to the allowlist
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

#Adds all the end points to the application
app.include_router(login_routes)
app.include_router(item_routes)
app.include_router(bid_routes)
app.include_router(transaction_routes)
app.include_router(rating_routes)