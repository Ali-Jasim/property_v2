from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    landlord_id = Column(Integer, ForeignKey("landlords.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    
    # Update the relationship reference to match the property model
    landlord = relationship("Landlord", back_populates="tenants")
    property = relationship("Property", back_populates="tenant")
    
    def __repr__(self):
        return f"<Tenant(name='{self.name}', email='{self.email}'), phone_number='{self.phone_number}'>"
