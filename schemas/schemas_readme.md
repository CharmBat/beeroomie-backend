# Schemas Folder
The schemas folder in a FastAPI project contains all the Pydantic models (schemas) used for request and response validation. These schemas define the structure of the data expected from incoming requests and outgoing responses, helping to ensure data integrity and simplify validation by enforcing data types, required fields, and constraints.

By organizing Pydantic schemas in this folder, you achieve a cleaner codebase where data validation logic is separated from business logic, making it easier to maintain and scale.

## Folder Structure
Each file in the schemas folder often represents a specific resource or feature. For instance, if your application has User and Item resources, you might have user.py and item.py files under schemas.

### Example Folder Structure
```
project_name/
├── app/
│   ├── schemas/
│   │   ├── user.py         # Pydantic schemas for user-related data
│   │   ├── item.py         # Pydantic schemas for item-related data
```
### Example Schema
Below is an example schema definition for user-related data. This includes a **UserCreate** schema for validating incoming data when creating a user, and a **UserResponse** schema for controlling the structure of data returned in API responses.

user.py Example
```
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    
    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
    Schema for the user data returned in responses.
    
    Attributes:
        id (int): The unique identifier of the user.
        email (EmailStr): The user's email address.
    """
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
```
## Explanation

---


UserCreate:
- Used to validate the incoming data when creating a new user.

---


Fields:
- email: An **EmailStr** field (provided by Pydantic) to validate that the email format is correct.
- password: A str field for the user’s password.


---


UserResponse:
- Used to define the data returned in API responses.


---


Fields:
- id: An int representing the unique identifier of the user.
- email: An EmailStr field for the user’s email.

  
---


Config:
- The Config class includes orm_mode = True, which allows Pydantic to work seamlessly with SQLAlchemy models, making it possible to return database objects directly as response data.


---

## Usage
These schemas can be used in the routers and crud layers to enforce validation and structure for request and response data.

For instance, in a route to create a new user:

```
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user
from app.db.session import get_db

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return db_user
```
This route will validate incoming requests against the UserCreate schema and return responses formatted according to the UserResponse schema.

Organizing Pydantic schemas in the schemas folder keeps the code modular, with a clear separation of validation logic, making it easier to understand, test, and extend.