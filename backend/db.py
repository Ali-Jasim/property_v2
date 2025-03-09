from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models.base import Base
from models.tenant import Tenant
from models.landlord import Landlord
from models.contractor import Contractor
from models.property import Property

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./property_management.db"
# Uncomment and adjust for production database:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/property_management"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Tenant CRUD operations
def create_tenant(db: Session, tenant_data: dict):
    tenant = Tenant(**tenant_data)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

def get_tenant(db: Session, tenant_id: int):
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()

def get_tenants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tenant).offset(skip).limit(limit).all()

def update_tenant(db: Session, tenant_id: int, tenant_data: dict):
    tenant = get_tenant(db, tenant_id)
    if tenant:
        for key, value in tenant_data.items():
            setattr(tenant, key, value)
        db.commit()
        db.refresh(tenant)
    return tenant

def delete_tenant(db: Session, tenant_id: int):
    tenant = get_tenant(db, tenant_id)
    if tenant:
        db.delete(tenant)
        db.commit()
        return True
    return False

# Landlord CRUD operations
def create_landlord(db: Session, landlord_data: dict):
    landlord = Landlord(**landlord_data)
    db.add(landlord)
    db.commit()
    db.refresh(landlord)
    return landlord

def get_landlord(db: Session, landlord_id: int):
    return db.query(Landlord).filter(Landlord.id == landlord_id).first()

def get_landlords(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Landlord).offset(skip).limit(limit).all()

def update_landlord(db: Session, landlord_id: int, landlord_data: dict):
    landlord = get_landlord(db, landlord_id)
    if landlord:
        for key, value in landlord_data.items():
            setattr(landlord, key, value)
        db.commit()
        db.refresh(landlord)
    return landlord

def delete_landlord(db: Session, landlord_id: int):
    landlord = get_landlord(db, landlord_id)
    if landlord:
        db.delete(landlord)
        db.commit()
        return True
    return False

# Contractor CRUD operations
def create_contractor(db: Session, contractor_data: dict):
    # Make a copy of the data to avoid modifying the original
    data = contractor_data.copy()
    
    # No need to manually convert work to JSON since the hybrid property handles it
    
    contractor = Contractor(**data)
    db.add(contractor)
    db.commit()
    db.refresh(contractor)
    return contractor

def get_contractor(db: Session, contractor_id: int):
    return db.query(Contractor).filter(Contractor.id == contractor_id).first()

def get_contractors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contractor).offset(skip).limit(limit).all()

def update_contractor(db: Session, contractor_id: int, contractor_data: dict):
    contractor = get_contractor(db, contractor_id)
    if contractor:
        # No need to manually convert work to JSON since the hybrid property handles it
        for key, value in contractor_data.items():
            setattr(contractor, key, value)
        db.commit()
        db.refresh(contractor)
    return contractor

def delete_contractor(db: Session, contractor_id: int):
    contractor = get_contractor(db, contractor_id)
    if contractor:
        db.delete(contractor)
        db.commit()
        return True
    return False

# Property CRUD operations
def create_property(db: Session, property_data: dict):
    property_obj = Property(**property_data)
    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)
    return property_obj

def get_property(db: Session, property_id: int):
    return db.query(Property).filter(Property.id == property_id).first()

def get_properties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Property).offset(skip).limit(limit).all()

def update_property(db: Session, property_id: int, property_data: dict):
    property_obj = get_property(db, property_id)
    if property_obj:
        for key, value in property_data.items():
            setattr(property_obj, key, value)
        db.commit()
        db.refresh(property_obj)
    return property_obj

def delete_property(db: Session, property_id: int):
    property_obj = get_property(db, property_id)
    if property_obj:
        db.delete(property_obj)
        db.commit()
        return True
    return False

# Relationship operations
def get_landlord_properties(db: Session, landlord_id: int):
    return db.query(Property).filter(Property.landlord_id == landlord_id).all()

def get_property_tenant(db: Session, property_id: int):
    return db.query(Tenant).filter(Tenant.property_id == property_id).first()

def get_property_tenants(db: Session, property_id: int):
    tenant = get_property_tenant(db, property_id)
    return [tenant] if tenant else []

def get_landlord_tenants(db: Session, landlord_id: int):
    return db.query(Tenant).filter(Tenant.landlord_id == landlord_id).all()

def get_landlord_contractors(db: Session, landlord_id: int):
    return db.query(Contractor).filter(Contractor.landlord_id == landlord_id).all()
