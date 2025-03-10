# Property Management System

This project is a property management system built with FastAPI and SQLAlchemy. It includes models and endpoints for managing tenants, contractors, landlords, and properties.

## Models

### Tenant

Represents a tenant in the system.

- **Attributes:**

  - `id` (int): Primary key.
  - `name` (str): Name of the tenant.
  - `phone_number` (str): Phone number of the tenant.
  - `email` (str): Email address of the tenant.
  - `landlord_id` (int): Foreign key referencing the landlord.
  - `property_id` (int, optional): Foreign key referencing the property.

- **Relationships:**
  - `landlord`: Many-to-one relationship with the `Landlord` model.
  - `property`: One-to-one relationship with the `Property` model.

### Contractor

Represents a contractor in the system.

- **Attributes:**

  - `id` (int): Primary key.
  - `name` (str): Name of the contractor.
  - `phone_number` (str): Phone number of the contractor.
  - `email` (str): Email address of the contractor.
  - `_work` (str): JSON string representing the work details.
  - `landlord_id` (int): Foreign key referencing the landlord.

- **Relationships:**

  - `landlord`: Many-to-one relationship with the `Landlord` model.

- **Properties:**
  - `work` (list): List of work details, stored as a JSON string.

### Landlord

Represents a landlord in the system.

- **Attributes:**

  - `id` (int): Primary key.
  - `name` (str): Name of the landlord.
  - `phone_number` (str): Phone number of the landlord.
  - `email` (str): Email address of the landlord.

- **Relationships:**
  - `tenants`: One-to-many relationship with the `Tenant` model.
  - `contractors`: One-to-many relationship with the `Contractor` model.
  - `properties`: One-to-many relationship with the `Property` model.

### Property

Represents a property in the system.

- **Attributes:**

  - `id` (int): Primary key.
  - `address` (str): Address of the property.
  - `landlord_id` (int): Foreign key referencing the landlord.

- **Relationships:**
  - `landlord`: Many-to-one relationship with the `Landlord` model.
  - `tenant`: One-to-one relationship with the `Tenant` model.

## Endpoints

### Tenant Endpoints

- `POST /tenants/`: Create a new tenant.
- `GET /tenants/{tenant_id}`: Get a tenant by ID.
- `GET /tenants/`: Get all tenants with pagination.
- `PUT /tenants/{tenant_id}`: Update a tenant by ID.
- `DELETE /tenants/{tenant_id}`: Delete a tenant by ID.

### Contractor Endpoints

- `POST /contractors/`: Create a new contractor.
- `GET /contractors/{contractor_id}`: Get a contractor by ID.
- `GET /contractors/`: Get all contractors with pagination.
- `PUT /contractors/{contractor_id}`: Update a contractor by ID.
- `DELETE /contractors/{contractor_id}`: Delete a contractor by ID.

### Landlord Endpoints

- `POST /landlords/`: Create a new landlord.
- `GET /landlords/{landlord_id}`: Get a landlord by ID.
- `GET /landlords/`: Get all landlords with pagination.
- `PUT /landlords/{landlord_id}`: Update a landlord by ID.
- `DELETE /landlords/{landlord_id}`: Delete a landlord by ID.

### Property Endpoints

- `POST /properties/`: Create a new property.
- `GET /properties/{property_id}`: Get a property by ID.
- `GET /properties/`: Get all properties with pagination.
- `PUT /properties/{property_id}`: Update a property by ID.
- `DELETE /properties/{property_id}`: Delete a property by ID.

## Running the Application

To run the application, use the following command:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

This will start the FastAPI server on `http://0.0.0.0:8000`.
