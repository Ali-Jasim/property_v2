import json
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from models.base import Base

class Contractor(Base):
    __tablename__ = "contractors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    _work = Column("work", Text, nullable=False)  # Store as JSON string
    landlord_id = Column(Integer, ForeignKey("landlords.id"), nullable=False)
    
    # Use string references (already using strings)
    landlord = relationship("Landlord", back_populates="contractors")
    
    @hybrid_property
    def work(self):
        """Convert JSON string to list when accessing the property"""
        return json.loads(self._work)
    
    @work.setter
    def work(self, work_list):
        """Convert list to JSON string when setting the property"""
        self._work = json.dumps(work_list)
    
    def __repr__(self):
        return f"<Contractor(name='{self.name}', email='{self.email}', phone_number='{self.phone_number}')>"
