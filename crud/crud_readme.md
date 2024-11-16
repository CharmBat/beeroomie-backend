# CRUD Folder
The crud folder in a FastAPI project is intended to contain all functions responsible for interacting with the database. This includes creating, reading, updating, and deleting (CRUD) records in database tables. By organizing CRUD operations in this folder, we achieve cleaner and more modular code, as database operations are separated from business logic and route definitions.

## Folder Structure
Each file in the crud folder typically represents a database model, such as **user.py**, **item.py**, or **post.py**. This approach makes it easy to locate and modify CRUD operations for specific models as the project scales.

### Example Folder Structure

```
project_name/
├── app/
│   ├── crud/
│   │   ├── user.py         # CRUD operations related to the User model
│   │   ├── item.py         # CRUD operations related to the Item model
│   │   └── post.py         # CRUD operations related to the Post model
```
### Example CRUD Function
Here is an example of a CRUD function to create a new user in the database. It uses SQLAlchemy for database interactions and a Pydantic schema for data validation.

user.py Example
```
from sqlalchemy.orm import Session
from app.models.user import User  # Import the User SQLAlchemy model
from app.schemas.user import UserCreate  # Import the Pydantic schema for user creation

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## Usage
The create_user function can be called from route handlers or service functions to add a new user to the database.

By centralizing CRUD operations in the crud folder, we maintain clean separation between database interactions, business logic, and API routes. This organization also makes testing and modifying database operations easier.