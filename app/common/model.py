from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.common.database_conn import Base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func
from passlib.context import CryptContext


pwd = CryptContext(schemes=["argon2"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, unique=True, nullable=True)

    password = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)

    createdOn = Column(DateTime, default=func.now())

    # Relationship
    profile = relationship ("ProfileTable", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def verify_password(self, plain_password: str):
        return pwd.verify(plain_password, self.password)

    def set_password(self, plain_password: str):
        self.password = pwd.hash(plain_password)


class ProfileTable(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    dateOfBirth = Column(Date, nullable=True)
    designation = Column(String, nullable=True)
    companyName = Column(String, nullable=True)
    profileImage = Column(String, nullable=True)
    image_public_id = Column(String, nullable=True)
    createdOn = Column(DateTime, default=func.now())
    updatedOn = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="profile")



class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    userName = Column(String(100), nullable=False)
    designation = Column(String(100), nullable=False)
    companyName = Column(String(150), default=None,nullable=False)
    image = Column(String(255), nullable=True)
    rating = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=False)
    createdOn = Column(DateTime(timezone=True), server_default=func.now())


# forget password table
class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())