from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String(40), unique=True, index=True)
    message = Column(String(500))
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    parent_hash = Column(String(40), nullable=True)

    # Relationships
    author = relationship("User", back_populates="commits")
    files = relationship("File", back_populates="commit")

    def __repr__(self):
        return f"<Commit {self.hash[:8]}>"

    @property
    def short_hash(self):
        return self.hash[:8]