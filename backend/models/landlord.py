from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session

from models.base import Base

class Landlord(Base):
    __tablename__ = "landlords"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    
    # Use string references for relationships
    tenants = relationship("Tenant", back_populates="landlord")
    contractors = relationship("Contractor", back_populates="landlord")
    properties = relationship("Property", back_populates="landlord")
    
    def __repr__(self):
        return f"<Landlord(name='{self.name}', email='{self.email}', phone_number='{self.phone_number}')>"
    
    @staticmethod
    def create(db: Session, landlord_data: dict):
        landlord = Landlord(**landlord_data)
        db.add(landlord)
        db.commit()
        db.refresh(landlord)
        return landlord

    @staticmethod
    def get(db: Session, landlord_id: int):
        return db.query(Landlord).filter(Landlord.id == landlord_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Landlord).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, landlord_id: int, landlord_data: dict):
        landlord = Landlord.get(db, landlord_id)
        if landlord:
            for key, value in landlord_data.items():
                setattr(landlord, key, value)
            db.commit()
            db.refresh(landlord)
        return landlord

    @staticmethod
    def delete(db: Session, landlord_id: int):
        landlord = Landlord.get(db, landlord_id)
        if landlord:
            db.delete(landlord)
            db.commit()
            return True
        return False
