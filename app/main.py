from fastapi import FastAPI

from app.routers.user import user
from app.routers.profile import profile
from app.common.database_conn import Base, engine
from app.routers.feedBack import feedback

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(user.router)
app.include_router(profile.router)
app.include_router(feedback.router)
