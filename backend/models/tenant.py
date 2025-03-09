from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

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
    
    @staticmethod
    def create(db: Session, tenant_data: dict):
        tenant = Tenant(**tenant_data)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        return tenant

    @staticmethod
    def get(db: Session, tenant_id: int):
        return db.query(Tenant).filter(Tenant.id == tenant_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Tenant).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, tenant_id: int, tenant_data: dict):
        tenant = Tenant.get(db, tenant_id)
        if tenant:
            for key, value in tenant_data.items():
                setattr(tenant, key, value)
            db.commit()
            db.refresh(tenant)
        return tenant

    @staticmethod
    def delete(db: Session, tenant_id: int):
        tenant = Tenant.get(db, tenant_id)
        if tenant:
            db.delete(tenant)
            db.commit()
            return True
        return False
