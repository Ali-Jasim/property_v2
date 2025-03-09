from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

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
    
    @staticmethod
    def create(db: Session, property_data: dict):
        property_obj = Property(**property_data)
        db.add(property_obj)
        db.commit()
        db.refresh(property_obj)
        return property_obj

    @staticmethod
    def get(db: Session, property_id: int):
        return db.query(Property).filter(Property.id == property_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Property).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, property_id: int, property_data: dict):
        property_obj = Property.get(db, property_id)
        if property_obj:
            for key, value in property_data.items():
                setattr(property_obj, key, value)
            db.commit()
            db.refresh(property_obj)
        return property_obj

    @staticmethod
    def delete(db: Session, property_id: int):
        property_obj = Property.get(db, property_id)
        if property_obj:
            db.delete(property_obj)
            db.commit()
            return True
        return False
