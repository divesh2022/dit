from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(255), index=True)
    status = Column(String(50))  # new, modified, deleted, unchanged
    hash = Column(String(64))  # MD5 hash of file content
    last_modified = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    commit_id = Column(Integer, ForeignKey("commits.id"))

    # Relationships
    user = relationship("User", back_populates="files")
    commit = relationship("Commit", back_populates="files")

    def __repr__(self):
        return f"<File {self.path} ({self.status})>"