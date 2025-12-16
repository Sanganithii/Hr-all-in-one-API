from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import user
from app.routers.profile import profile
from app.common.database_conn import Base, engine
from app.routers.feedBack import feedback
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["POST","PUT","GET"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
Base.metadata.create_all(bind=engine)


app.include_router(user.router)
app.include_router(profile.router)
app.include_router(feedback.router)
