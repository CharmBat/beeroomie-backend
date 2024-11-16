# Routers Folder
The routers folder in a FastAPI project is designed to contain all API route definitions for the application. These routes map incoming HTTP requests to specific handlers, such as CRUD functions or business logic, making it easy to organize endpoints by feature or resource. By organizing routes in this folder, the codebase stays modular and maintainable as the application grows.

## Folder Structure
The routers folder typically contains separate files for each resource or feature of the application. For instance, if your application has **User** and **Item** resources, you might have **user.py** and **item.py** files in the routers folder.

### Example Folder Structure
```
project_name/
├── app/
│   ├── routers/
│   │   ├── user.py         # Routes for user-related endpoints
│   │   ├── item.py         # Routes for item-related endpoints
```
### Example Route
Here’s an example of a route definition for user-related operations, specifically for creating a new user. This route handles POST requests to the **/users/** endpoint, validates the request body with a Pydantic schema, and calls a CRUD function to save the user data to the database.

user.py Example
```
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user
from app.db.session import get_db

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """
    Route to create a new user in the database.

    Args:
        user (UserCreate): The user data validated by the UserCreate schema.
        db (Session): Database session, provided by dependency injection.

    Returns:
        UserResponse: The created user data as a response model.
    """
    db_user = create_user(db=db, user=user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User could not be created.")
    return db_user
```

## Usage
To use this route, include it in the main FastAPI app in main.py:

```
from fastapi import FastAPI
from app.routers import user

app = FastAPI()

app.include_router(user.router)
```
This registers the user routes with the main FastAPI application, making the /users/ endpoint available.

Organizing API routes in the routers folder helps keep route definitions separate from business logic and database operations, making the code more modular and easier to maintain.