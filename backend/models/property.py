from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)  # Location information
    landlord_id = Column(Integer, ForeignKey("landlords.id"), nullable=False)
    
    # Change relationship with tenant from one-to-many to one-to-one
    landlord = relationship("Landlord", back_populates="properties")
    tenant = relationship("Tenant", back_populates="property", uselist=False)
    
    def __repr__(self):
        return f"<Property(address='{self.address}')>"
