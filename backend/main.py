from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.Login import login_routes
from backend.database import create_db_and_tables


app = FastAPI()


#starting the server and creating tables
@app.on_event('startup')
def startup():
    create_db_and_tables()

origins = ["http://localhost:5173"]

#Added the local react server to the allowlist
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

#Adds all the end points to the application
app.include_router(login_routes)