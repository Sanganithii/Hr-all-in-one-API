from fastapi import FastAPI

from routers.user import user
from routers.profile import profile
from common.database_conn import Base, engine
from routers.feedBack import feedback

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(user.router)
app.include_router(profile.router)
app.include_router(feedback.router)
