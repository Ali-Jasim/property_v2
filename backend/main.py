import uvicorn
from api import app
from db import create_tables

if __name__ == "__main__":
    # Create database tables before starting the server
    create_tables()
    print("Database tables created successfully!")
    
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
