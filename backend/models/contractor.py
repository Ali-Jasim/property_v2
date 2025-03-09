import json
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, Session
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
    
    @staticmethod
    def create(db: Session, contractor_data: dict):
        contractor = Contractor(**contractor_data)
        db.add(contractor)
        db.commit()
        db.refresh(contractor)
        return contractor

    @staticmethod
    def get(db: Session, contractor_id: int):
        return db.query(Contractor).filter(Contractor.id == contractor_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Contractor).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, contractor_id: int, contractor_data: dict):
        contractor = Contractor.get(db, contractor_id)
        if contractor:
            for key, value in contractor_data.items():
                setattr(contractor, key, value)
            db.commit()
            db.refresh(contractor)
        return contractor

    @staticmethod
    def delete(db: Session, contractor_id: int):
        contractor = Contractor.get(db, contractor_id)
        if contractor:
            db.delete(contractor)
            db.commit()
            return True
        return False
