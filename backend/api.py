from fastapi import FastAPI, Depends, HTTPException, status, Request, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from db import (
    get_db, create_tenant, get_tenant, get_tenants, update_tenant, delete_tenant,
    create_landlord, get_landlord, get_landlords, update_landlord, delete_landlord,
    create_contractor, get_contractor, get_contractors, update_contractor, delete_contractor,
    create_property, get_property, get_properties, update_property, delete_property,
    get_landlord_properties, get_property_tenants, get_landlord_tenants, get_landlord_contractors,
    create_tables  # Import the create_tables function
)
from models.tenant import Tenant  # Correct import for the Tenant model

app = FastAPI(title="Property Management API")

# Create all database tables on startup
@app.on_event("startup")
def on_startup():
    create_tables()
    print("Database tables created successfully!")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Property Management API"}

# Helper function to convert SQLAlchemy objects to dictionaries
def to_dict(obj):
    result = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    
    # Special handling for Contractor's work attribute
    if hasattr(obj, '__tablename__') and obj.__tablename__ == 'contractors':
        # Replace _work with the converted work list
        if '_work' in result:
            result['work'] = obj.work
            del result['_work']
    
    return result

# Tenant routes
@app.post("/tenants/", status_code=status.HTTP_201_CREATED)
async def create_tenant_endpoint(
    name: str = Body(..., description="Tenant's full name"),
    phone_number: str = Body(..., description="Tenant's phone number"),
    email: str = Body(..., description="Tenant's email address"),
    landlord_id: int = Body(..., description="ID of the landlord"),
    property_id: Optional[int] = Body(None, description="ID of the property (optional)"),
    db: Session = Depends(get_db)
):
    tenant_data = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "landlord_id": landlord_id,
        "property_id": property_id
    }
    try:
        tenant = create_tenant(db=db, tenant_data=tenant_data)
        return to_dict(tenant)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tenants/")
def read_tenants(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    name: Optional[str] = Query(None, description="Filter by name"),
    landlord_id: Optional[int] = Query(None, description="Filter by landlord ID"),
    property_id: Optional[int] = Query(None, description="Filter by property ID"),
    db: Session = Depends(get_db)
):
    tenants = get_tenants(db, skip=skip, limit=limit)
    
    # Apply filters if provided
    if name:
        tenants = [t for t in tenants if name.lower() in t.name.lower()]
    if landlord_id:
        tenants = [t for t in tenants if t.landlord_id == landlord_id]
    if property_id:
        tenants = [t for t in tenants if t.property_id == property_id]
        
    return [to_dict(tenant) for tenant in tenants]

@app.get("/tenants/{tenant_id}")
def read_tenant(
    tenant_id: int = Path(..., description="The ID of the tenant to get"),
    db: Session = Depends(get_db)
):
    db_tenant = get_tenant(db, tenant_id=tenant_id)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return to_dict(db_tenant)

@app.put("/tenants/{tenant_id}")
async def update_tenant_endpoint(
    tenant_id: int = Path(..., description="The ID of the tenant to update"),
    name: Optional[str] = Body(None, description="Updated name"),
    phone_number: Optional[str] = Body(None, description="Updated phone number"),
    email: Optional[str] = Body(None, description="Updated email"),
    property_id: Optional[int] = Body(None, description="Updated property ID"),
    landlord_id: Optional[int] = Body(None, description="Updated landlord ID"),
    db: Session = Depends(get_db)
):
    tenant_data = {}
    if name is not None:
        tenant_data["name"] = name
    if phone_number is not None:
        tenant_data["phone_number"] = phone_number
    if email is not None:
        tenant_data["email"] = email
    if property_id is not None:
        tenant_data["property_id"] = property_id
    if landlord_id is not None:
        tenant_data["landlord_id"] = landlord_id

    db_tenant = update_tenant(db, tenant_id=tenant_id, tenant_data=tenant_data)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return to_dict(db_tenant)

@app.delete("/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant_endpoint(
    tenant_id: int = Path(..., description="The ID of the tenant to delete"),
    db: Session = Depends(get_db)
):
    success = delete_tenant(db, tenant_id=tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return None

# Landlord routes
@app.post("/landlords/", status_code=status.HTTP_201_CREATED)
async def create_landlord_endpoint(
    name: str = Body(..., description="Landlord's full name"),
    phone_number: str = Body(..., description="Landlord's phone number"),
    email: str = Body(..., description="Landlord's email address"),
    db: Session = Depends(get_db)
):
    landlord_data = {
        "name": name,
        "phone_number": phone_number,
        "email": email
    }
    try:
        landlord = create_landlord(db=db, landlord_data=landlord_data)
        return to_dict(landlord)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/landlords/")
def read_landlords(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    name: Optional[str] = Query(None, description="Filter by name"),
    db: Session = Depends(get_db)
):
    landlords = get_landlords(db, skip=skip, limit=limit)
    
    # Apply filters if provided
    if name:
        landlords = [l for l in landlords if name.lower() in l.name.lower()]
        
    return [to_dict(landlord) for landlord in landlords]

@app.get("/landlords/{landlord_id}")
def read_landlord(
    landlord_id: int = Path(..., description="The ID of the landlord to get"),
    db: Session = Depends(get_db)
):
    db_landlord = get_landlord(db, landlord_id=landlord_id)
    if db_landlord is None:
        raise HTTPException(status_code=404, detail="Landlord not found")
    return to_dict(db_landlord)

@app.put("/landlords/{landlord_id}")
async def update_landlord_endpoint(
    landlord_id: int = Path(..., description="The ID of the landlord to update"),
    name: Optional[str] = Body(None, description="Updated name"),
    phone_number: Optional[str] = Body(None, description="Updated phone number"),
    email: Optional[str] = Body(None, description="Updated email"),
    db: Session = Depends(get_db)
):
    landlord_data = {}
    if name is not None:
        landlord_data["name"] = name
    if phone_number is not None:
        landlord_data["phone_number"] = phone_number
    if email is not None:
        landlord_data["email"] = email

    db_landlord = update_landlord(db, landlord_id=landlord_id, landlord_data=landlord_data)
    if db_landlord is None:
        raise HTTPException(status_code=404, detail="Landlord not found")
    return to_dict(db_landlord)

@app.delete("/landlords/{landlord_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_landlord_endpoint(
    landlord_id: int = Path(..., description="The ID of the landlord to delete"),
    db: Session = Depends(get_db)
):
    success = delete_landlord(db, landlord_id=landlord_id)
    if not success:
        raise HTTPException(status_code=404, detail="Landlord not found")
    return None

# Contractor routes
@app.post("/contractors/", status_code=status.HTTP_201_CREATED)
async def create_contractor_endpoint(
    name: str = Body(..., description="Contractor's full name"),
    phone_number: str = Body(..., description="Contractor's phone number"),
    email: str = Body(..., description="Contractor's email address"),
    work: List[str] = Body(..., description="List of work types the contractor does"),
    landlord_id: int = Body(..., description="ID of the landlord"),
    db: Session = Depends(get_db)
):
    contractor_data = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "work": work,
        "landlord_id": landlord_id
    }
    try:
        contractor = create_contractor(db=db, contractor_data=contractor_data)
        return to_dict(contractor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/contractors/")
def read_contractors(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    name: Optional[str] = Query(None, description="Filter by name"),
    work_type: Optional[str] = Query(None, description="Filter by work type"),
    landlord_id: Optional[int] = Query(None, description="Filter by landlord ID"),
    db: Session = Depends(get_db)
):
    contractors = get_contractors(db, skip=skip, limit=limit)
    
    # Apply filters if provided
    if name:
        contractors = [c for c in contractors if name.lower() in c.name.lower()]
    if work_type:
        contractors = [c for c in contractors if work_type.lower() in [w.lower() for w in c.work]]
    if landlord_id:
        contractors = [c for c in contractors if c.landlord_id == landlord_id]
        
    return [to_dict(contractor) for contractor in contractors]

@app.get("/contractors/{contractor_id}")
def read_contractor(
    contractor_id: int = Path(..., description="The ID of the contractor to get"),
    db: Session = Depends(get_db)
):
    db_contractor = get_contractor(db, contractor_id=contractor_id)
    if db_contractor is None:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return to_dict(db_contractor)

@app.put("/contractors/{contractor_id}")
async def update_contractor_endpoint(
    contractor_id: int = Path(..., description="The ID of the contractor to update"),
    name: Optional[str] = Body(None, description="Updated name"),
    phone_number: Optional[str] = Body(None, description="Updated phone number"),
    email: Optional[str] = Body(None, description="Updated email"),
    work: Optional[List[str]] = Body(None, description="Updated list of work types"),
    landlord_id: Optional[int] = Body(None, description="Updated landlord ID"),
    db: Session = Depends(get_db)
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

    db_contractor = update_contractor(db, contractor_id=contractor_id, contractor_data=contractor_data)
    if db_contractor is None:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return to_dict(db_contractor)

@app.delete("/contractors/{contractor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contractor_endpoint(
    contractor_id: int = Path(..., description="The ID of the contractor to delete"),
    db: Session = Depends(get_db)
):
    success = delete_contractor(db, contractor_id=contractor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return None

# Property routes
@app.post("/properties/", status_code=status.HTTP_201_CREATED)
async def create_property_endpoint(
    address: str = Body(..., description="Property address/location"),
    landlord_id: int = Body(..., description="ID of the landlord"),
    db: Session = Depends(get_db)
):
    property_data = {
        "address": address,
        "landlord_id": landlord_id
    }
    try:
        property_obj = create_property(db=db, property_data=property_data)
        return to_dict(property_obj)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/properties/")
def read_properties(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    address: Optional[str] = Query(None, description="Filter by address"),
    landlord_id: Optional[int] = Query(None, description="Filter by landlord ID"),
    db: Session = Depends(get_db)
):
    properties = get_properties(db, skip=skip, limit=limit)
    
    # Apply filters if provided
    if address:
        properties = [p for p in properties if address.lower() in p.address.lower()]
    if landlord_id:
        properties = [p for p in properties if p.landlord_id == landlord_id]
        
    return [to_dict(prop) for prop in properties]

@app.get("/properties/{property_id}")
def read_property(
    property_id: int = Path(..., description="The ID of the property to get"),
    db: Session = Depends(get_db)
):
    db_property = get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return to_dict(db_property)

@app.put("/properties/{property_id}")
async def update_property_endpoint(
    property_id: int = Path(..., description="The ID of the property to update"),
    address: Optional[str] = Body(None, description="Updated address"),
    landlord_id: Optional[int] = Body(None, description="Updated landlord ID"),
    db: Session = Depends(get_db)
):
    property_data = {}
    if address is not None:
        property_data["address"] = address
    if landlord_id is not None:
        property_data["landlord_id"] = landlord_id

    db_property = update_property(db, property_id=property_id, property_data=property_data)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return to_dict(db_property)

@app.delete("/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_endpoint(
    property_id: int = Path(..., description="The ID of the property to delete"),
    db: Session = Depends(get_db)
):
    success = delete_property(db, property_id=property_id)
    if not success:
        raise HTTPException(status_code=404, detail="Property not found")
    return None

# Relationship routes
@app.get("/landlords/{landlord_id}/properties")
def read_landlord_properties_endpoint(
    landlord_id: int = Path(..., description="The ID of the landlord"),
    db: Session = Depends(get_db)
):
    db_landlord = get_landlord(db, landlord_id=landlord_id)
    if db_landlord is None:
        raise HTTPException(status_code=404, detail="Landlord not found")
    properties = get_landlord_properties(db, landlord_id=landlord_id)
    return [to_dict(prop) for prop in properties]

@app.get("/landlords/{landlord_id}/tenants")
def read_landlord_tenants_endpoint(
    landlord_id: int = Path(..., description="The ID of the landlord"),
    db: Session = Depends(get_db)
):
    db_landlord = get_landlord(db, landlord_id=landlord_id)
    if db_landlord is None:
        raise HTTPException(status_code=404, detail="Landlord not found")
    tenants = get_landlord_tenants(db, landlord_id=landlord_id)
    return [to_dict(tenant) for tenant in tenants]

@app.get("/landlords/{landlord_id}/contractors")
def read_landlord_contractors_endpoint(
    landlord_id: int = Path(..., description="The ID of the landlord"),
    db: Session = Depends(get_db)
):
    db_landlord = get_landlord(db, landlord_id=landlord_id)
    if db_landlord is None:
        raise HTTPException(status_code=404, detail="Landlord not found")
    contractors = get_landlord_contractors(db, landlord_id=landlord_id)
    return [to_dict(contractor) for contractor in contractors]

@app.get("/properties/{property_id}/tenant")
def read_property_tenant_endpoint(
    property_id: int = Path(..., description="The ID of the property"),
    db: Session = Depends(get_db)
):
    db_property = get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Get the single tenant for this property
    tenant = db.query(Tenant).filter(Tenant.property_id == property_id).first()
    if tenant is None:
        return None
    return to_dict(tenant)

# Update the existing endpoint to maintain backward compatibility
@app.get("/properties/{property_id}/tenants")
def read_property_tenants_endpoint(
    property_id: int = Path(..., description="The ID of the property"),
    db: Session = Depends(get_db)
):
    # Call the newer endpoint for a single tenant
    return read_property_tenant_endpoint(property_id, db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
