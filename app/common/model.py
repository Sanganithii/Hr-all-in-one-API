from sqlalchemy import Column, Date, Integer, String, Text
from app.common.database_conn import Base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func
from passlib.context import CryptContext


pwd = CryptContext(schemes=["argon2"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    createdOn = Column(DateTime, default=func.now())         
    phone = Column(String, nullable=True)
   
    def verify_password(self, plain_password: str):
        return pwd.verify(plain_password, self.password)

    def set_password(self, plain_password: str):
        self.password = pwd.hash(plain_password)


 
class ProfileTable(Base):
    __tablename__ = "profileTable"
    
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    dateOfBirth = Column(Date, nullable=True)
    designation = Column(String, nullable=False)
    companyName = Column(String, nullable=True)
    profileImage = Column(String, nullable=True)
    createdOn = Column(DateTime, nullable=False)
    updatedOn = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)



class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)

    # userId = Column(Integer, ForeignKey("users.id"), nullable=False)
    userId = Column(Integer, nullable=False)

    userName = Column(String(100), nullable=False)
    designation = Column(String(100), nullable=False)
    companyName = Column(String(150), default=None,nullable=False)
    image = Column(String(255), nullable=True)

    rating = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=False)

    createdOn = Column(DateTime(timezone=True), server_default=func.now())

    # user = relationship("User", backref="feedbacks")
