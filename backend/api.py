from fastapi import FastAPI, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from models.base import Base
from models.tenant import Tenant
from models.contractor import Contractor
from models.landlord import Landlord
from models.property import Property
from database import SessionLocal, engine  # Updated import
from middleware.cors_middleware import setup_cors
import json

app = FastAPI()

setup_cors(app)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tenant endpoints
@app.post("/tenants/")
async def create_tenant(
    name: str = Query(...),
    phone_number: str = Query(...),
    email: str = Query(...),
    landlord_id: int = Query(...),
    db: Session = Depends(get_db),
):
    tenant_data = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "landlord_id": landlord_id,
    }
    return Tenant.create(db, tenant_data)


@app.get("/tenants/{tenant_id}")
def read_tenant(tenant_id: int, db: Session = Depends(get_db)):
    tenant = Tenant.get(db, tenant_id)
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@app.get("/tenants/")
def read_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return Tenant.get_all(db, skip, limit)


@app.put("/tenants/{tenant_id}")
def update_tenant(
    tenant_id: int,
    name: str = Query(None),
    phone_number: str = Query(None),
    email: str = Query(None),
    landlord_id: int = Query(None),
    db: Session = Depends(get_db),
):
    tenant_data = {}
    if name is not None:
        tenant_data["name"] = name
    if phone_number is not None:
        tenant_data["phone_number"] = phone_number
    if email is not None:
        tenant_data["email"] = email
    if landlord_id is not None:
        tenant_data["landlord_id"] = landlord_id

    tenant = Tenant.update(db, tenant_id, tenant_data)
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@app.delete("/tenants/{tenant_id}")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    if not Tenant.delete(db, tenant_id):
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"detail": "Tenant deleted"}


# Contractor endpoints
@app.post("/contractors/")
def create_contractor(
    name: str = Query(...),
    phone_number: str = Query(...),
    email: str = Query(...),
    work: str = Query(...),
    landlord_id: int = Query(None),
    db: Session = Depends(get_db),
):
    # Convert work to JSON string if it's not already
    contractor_data = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "work": work,  # Use 'work' instead of '_work' to match DB column name
        "landlord_id": landlord_id,
    }

    return Contractor.create(db, contractor_data)


@app.get("/contractors/{contractor_id}")
def read_contractor(contractor_id: int, db: Session = Depends(get_db)):
    contractor = Contractor.get(db, contractor_id)
    if contractor is None:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return contractor


@app.get("/contractors/")
def read_contractors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return Contractor.get_all(db, skip, limit)


@app.put("/contractors/{contractor_id}")
def update_contractor(
    contractor_id: int,
    name: str = Query(None),
    phone_number: str = Query(None),
    email: str = Query(None),
    work: str = Query(None),  # Added work parameter
    landlord_id: int = Query(None),  # Added landlord_id parameter
    db: Session = Depends(get_db),
):
    contractor_data = {}
    if name is not None:
        contractor_data["name"] = name
    if phone_number is not None:
        contractor_data["phone_number"] = phone_number
    if email is not None:
        contractor_data["email"] = email
    if work is not None:
        contractor_data["work"] = work
    if landlord_id is not None:
        contractor_data["landlord_id"] = landlord_id

    contractor = Contractor.update(db, contractor_id, contractor_data)
    if contractor is None:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return contractor


@app.delete("/contractors/{contractor_id}")
def delete_contractor(contractor_id: int, db: Session = Depends(get_db)):
    if not Contractor.delete(db, contractor_id):
        raise HTTPException(status_code=404, detail="Contractor not found")
    return {"detail": "Contractor deleted"}


# Landlord endpoints
@app.post("/landlords/")
def create_landlord(
    name: str = Query(...),
    phone_number: str = Query(...),
    email: str = Query(...),
    db: Session = Depends(get_db),
):
    landlord_data = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
    }
    return Landlord.create(db, landlord_data)


@app.get("/landlords/{landlord_id}")
def read_landlord(landlord_id: int, db: Session = Depends(get_db)):
    landlord = Landlord.get(db, landlord_id)
    if landlord is None:
        raise HTTPException(status_code=404, detail="Landlord not found")
    return landlord


@app.get("/landlords/")
def read_landlords(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return Landlord.get_all(db, skip, limit)


@app.put("/landlords/{landlord_id}")
def update_landlord(
    landlord_id: int,
    name: str = Query(None),
    phone_number: str = Query(None),
    email: str = Query(None),
    db: Session = Depends(get_db),
):
    landlord_data = {}
    if name is not None:
        landlord_data["name"] = name
    if phone_number is not None:
        landlord_data["phone_number"] = phone_number
    if email is not None:
        landlord_data["email"] = email

    landlord = Landlord.update(db, landlord_id, landlord_data)
    if landlord is None:
        raise HTTPException(status_code=404, detail="Landlord not found")
    return landlord


@app.delete("/landlords/{landlord_id}")
def delete_landlord(landlord_id: int, db: Session = Depends(get_db)):
    if not Landlord.delete(db, landlord_id):
        raise HTTPException(status_code=404, detail="Landlord not found")
    return {"detail": "Landlord deleted"}


# Property endpoints
@app.post("/properties/")
def create_property(
    address: str = Query(...),
    landlord_id: int = Query(...),
    db: Session = Depends(get_db),
):
    property_data = {"address": address, "landlord_id": landlord_id}
    return Property.create(db, property_data)


@app.get("/properties/{property_id}")
def read_property(property_id: int, db: Session = Depends(get_db)):
    property_obj = Property.get(db, property_id)
    if property_obj is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_obj


@app.get("/properties/")
def read_properties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return Property.get_all(db, skip, limit)


@app.put("/properties/{property_id}")
def update_property(
    property_id: int,
    address: str = Query(None),
    landlord_id: int = Query(None),
    db: Session = Depends(get_db),
):
    property_data = {}
    if address is not None:
        property_data["address"] = address
    if landlord_id is not None:
        property_data["landlord_id"] = landlord_id

    property_obj = Property.update(db, property_id, property_data)
    if property_obj is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_obj


@app.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    if not Property.delete(db, property_id):
        raise HTTPException(status_code=404, detail="Property not found")
    return {"detail": "Property deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
