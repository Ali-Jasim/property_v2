# Property Management System Backend

A FastAPI backend for managing properties, landlords, tenants, and contractors. This system provides a complete solution for property management with a RESTful API.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)
- [Data Models](#data-models)
- [Database Schema](#database-schema)
- [Example API Usage](#example-api-usage)

## Features

- Complete CRUD operations for:
  - Landlords
  - Tenants
  - Contractors
  - Properties
- Relationship management between entities
- Query filtering for all list endpoints
- SQLite database with SQLAlchemy ORM
- FastAPI for high-performance API endpoints

## Installation

### Requirements

- Python 3.8+
- pip package manager

### Setup

1. Clone the repository

```bash
git clone <repository-url>
cd property_v2/backend
```

2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

You can run the server using one of two methods:

### Method 1: Using uvicorn directly

```bash
uvicorn api:app --reload
```

### Method 2: Using the main.py script

```bash
python main.py
```

The server will start on http://localhost:8000. You can access the API documentation at http://localhost:8000/docs.

## API Documentation

FastAPI provides automatic interactive API documentation. Visit http://localhost:8000/docs after starting the server to explore all endpoints and test them interactively.

### Base URL

All API endpoints are available under `http://localhost:8000/`.

### Authentication

The API currently doesn't include authentication. This should be implemented before production use.

## Data Models

### Landlord

- `id`: Primary key
- `name`: Full name
- `phone_number`: Contact number
- `email`: Email address (unique)
- Relations: Has many tenants, contractors, and properties

### Tenant

- `id`: Primary key
- `name`: Full name
- `phone_number`: Contact number
- `email`: Email address (unique)
- `landlord_id`: Reference to landlord
- `property_id`: Optional reference to property
- Relations: Belongs to a landlord and optionally to a property

### Contractor

- `id`: Primary key
- `name`: Full name
- `phone_number`: Contact number
- `email`: Email address (unique)
- `work`: List of work types the contractor performs
- `landlord_id`: Reference to landlord
- Relations: Belongs to a landlord

### Property

- `id`: Primary key
- `address`: Full address
- `property_type`: Type (apartment, house, condo, etc.)
- `bedrooms`: Number of bedrooms
- `bathrooms`: Number of bathrooms
- `rent_amount`: Monthly rent
- `is_occupied`: Occupancy status
- `landlord_id`: Reference to landlord
- Relations: Belongs to a landlord, has many tenants

## Database Schema

The application uses SQLite by default, with tables created based on the SQLAlchemy models. The database file is created as `property_management.db` in the project root.

Entity relationships:

- One landlord has many properties
- One landlord has many tenants
- One landlord has many contractors
- One property has many tenants
- One tenant belongs to one landlord
- One tenant can belong to one property

## Example API Usage

### Landlords

#### Create a Landlord

```bash
curl -X POST http://localhost:8000/landlords/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Smith", "phone_number": "555-1234", "email": "john@example.com"}'
```

#### Get All Landlords

```bash
curl -X GET http://localhost:8000/landlords/
```

#### Get a Specific Landlord

```bash
curl -X GET http://localhost:8000/landlords/1
```

#### Update a Landlord

```bash
curl -X PUT http://localhost:8000/landlords/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John D. Smith", "phone_number": "555-5678"}'
```

#### Delete a Landlord

```bash
curl -X DELETE http://localhost:8000/landlords/1
```

### Properties

#### Create a Property

```bash
curl -X POST http://localhost:8000/properties/ \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Main St",
    "property_type": "apartment",
    "bedrooms": 2,
    "bathrooms": 1.5,
    "rent_amount": 1200,
    "is_occupied": false,
    "landlord_id": 1
  }'
```

#### Get Properties with Filtering

```bash
curl -X GET "http://localhost:8000/properties/?min_bedrooms=2&max_rent=1500&property_type=apartment"
```

### Tenants

#### Create a Tenant

```bash
curl -X POST http://localhost:8000/tenants/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "phone_number": "555-9876",
    "email": "jane@example.com",
    "landlord_id": 1,
    "property_id": 1
  }'
```

### Contractors

#### Create a Contractor

```bash
curl -X POST http://localhost:8000/contractors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fix-It Felix",
    "phone_number": "555-2468",
    "email": "felix@repair.com",
    "work": ["plumbing", "electrical", "carpentry"],
    "landlord_id": 1
  }'
```

### Relationship Queries

#### Get Properties for a Landlord

```bash
curl -X GET http://localhost:8000/landlords/1/properties
```

#### Get Tenants for a Property

```bash
curl -X GET http://localhost:8000/properties/1/tenants
```

## Development

### Project Structure

- `api.py`: FastAPI application and endpoints
- `db.py`: Database connection and CRUD operations
- `main.py`: Application entrypoint
- `models/`: SQLAlchemy model definitions
  - `base.py`: Base model class
  - `landlord.py`: Landlord model
  - `tenant.py`: Tenant model
  - `contractor.py`: Contractor model
  - `property.py`: Property model
- `requirements.txt`: Project dependencies

### Extending the API

To add a new entity:

1. Create a new model file in the `models/` directory
2. Add CRUD operations in `db.py`
3. Create API endpoints in `api.py`

### Production Considerations

For production deployment:

- Replace SQLite with a more robust database like PostgreSQL
- Add authentication and authorization
- Set up proper logging
- Configure CORS more restrictively
- Consider containerizing the application with Docker
