from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

from models.base import Base

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    property_type = Column(String, nullable=False)  # e.g. apartment, house, condo
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Float, nullable=False)
    rent_amount = Column(Float, nullable=False)
    is_occupied = Column(Boolean, default=False)
    landlord_id = Column(Integer, ForeignKey("landlords.id"), nullable=False)
    
    # Use string references (already using strings)
    landlord = relationship("Landlord", back_populates="properties")
    tenants = relationship("Tenant", back_populates="property")
    
    def __repr__(self):
        return f"<Property(address='{self.address}', type='{self.property_type}', occupied={self.is_occupied})>"
