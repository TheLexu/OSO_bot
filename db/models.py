from db.engine import Base
from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    vk_id = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    bdate = Column(Date)
    email = Column(String)
    phone_number = Column(String)
    is_male = Column(Boolean, default=True)

    events = relationship("Event", back_populates="owner")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="events")
