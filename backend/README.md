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
  - `property`: Many-to-one relationship with the `Property` model.

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
  - `properties`: Many-to-many relationship with the `Property` model through work assignments.

- **Properties:**
  - `work` (list): List of work details, accessed via getter/setter methods, stored as a JSON string.

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
  - `rent_amount` (float): Monthly rent amount.
  - `status` (str): Current status of the property (e.g., "vacant", "occupied").
  - `landlord_id` (int): Foreign key referencing the landlord.

- **Relationships:**
  - `landlord`: Many-to-one relationship with the `Landlord` model.
  - `tenants`: One-to-many relationship with the `Tenant` model.
  - `contractors`: Many-to-many relationship with the `Contractor` model through work assignments.

### Issue

Represents a maintenance or repair issue in the system.

- **Attributes:**

  - `id` (int): Primary key.
  - `description` (str): Description of the issue.
  - `location` (str): Location of the issue within the property.
  - `action` (str): Action to be taken to resolve the issue.
  - `resolved` (boolean): Status of the issue resolution.
  - `property_id` (int, optional): Foreign key referencing the property.

- **Relationships:**
  - `property`: Many-to-one relationship with the `Property` model.

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

### Issue Endpoints

- `POST /issues/`: Create a new issue.
- `GET /issues/{issue_id}`: Get an issue by ID.
- `GET /issues/`: Get all issues with pagination.
- `PUT /issues/{issue_id}`: Update an issue by ID.
- `DELETE /issues/{issue_id}`: Delete an issue by ID.

## Running the Application

To run the application, use the following command:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

This will start the FastAPI server on `http://0.0.0.0:8000`.

## File Structure

Key files in this project:

- `api.py`: Main FastAPI application with all endpoints
- `models/tenant.py`: Tenant model definition
- `models/contractor.py`: Contractor model definition
- `models/landlord.py`: Landlord model definition
- `models/property.py`: Property model definition
- `models/issue.py`: Issue model definition
