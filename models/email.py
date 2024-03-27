from sqlalchemy import Column, String, DateTime
from db.local_db import Base


class Email(Base):
    __tablename__ = 'emails'
    id = Column(String, primary_key=True)
    sender = Column(String)
    subject = Column(String)
    received_at = Column(DateTime)


