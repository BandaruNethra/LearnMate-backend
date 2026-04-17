from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime # Add ForeignKey and DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime # You'll also need this for the timestamp

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)  # Changed from username
    full_name = Column(String)
    hashed_password = Column(String)
    interests = Column(String)
    skill_level = Column(String)
    streak = Column(Integer, default=1)
    progress = Column(Integer, default=0)

    from sqlalchemy import ForeignKey # Add this import

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # 'user' or 'assistant'
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    thumbnail = Column(String) # URL to image
    video_url = Column(String) # The YouTube ID or internal video link
    category = Column(String)  # e.g., "Python", "Web Dev"

class Hackathon(Base):
    __tablename__ = "hackathons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    organizer = Column(String)
    date_text = Column(String)
    location = Column(String)
    link = Column(Text)
    prize = Column(String)
    tags = Column(String) # Store as "AI,Web3,Cloud"
    last_updated = Column(DateTime, default=datetime.utcnow)