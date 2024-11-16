# Models Folder
The models folder in a FastAPI project is designed to contain the SQLAlchemy models that define the structure of the database tables. These models represent the data tables and establish the schema for how data is stored and retrieved from the database. SQLAlchemy is typically used as the ORM (Object Relational Mapper) for defining these models, allowing us to interact with the database using Python objects instead of raw SQL queries.

## Folder Structure
Each file in the models folder often represents a database table or a closely related set of tables. For example, if the application has **User** and **Item** tables, the models folder might have **user.py** and **item.py** files. This organization keeps the codebase clean and helps scale as the number of models grows.

# Example Folder Structure
```
project_name/
├── app/
│   ├── models/
│   │   ├── user.py         # Model for the User table
│   │   ├── item.py         # Model for the Item table
```
# Example Database Model
Below is an example of a basic SQLAlchemy model for a User table. This model defines fields such as id, email, and hashed_password, and specifies the data types and constraints for each field.

user.py Example

```
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base  # Base class for all models

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
```
### Explanation
Attributes:

- id: This is an integer primary key that uniquely identifies each user.
- email: A string column that stores the user's email address, with constraints to ensure it is unique and indexed for faster lookups.
- hashed_password: A string column that stores the hashed password for user authentication.
Base Class:

Base: This is a common base class that all models inherit from. It’s typically defined in app/db/base_class.py and sets up SQLAlchemy's declarative_base() to enable table creation.
## Usage
The User model can be used in CRUD functions within the crud folder to create, read, update, and delete users in the database. For example, a create_user function in the crud/user.py file would accept a User instance and save it to the database.

By organizing models in the models folder, we maintain a clear structure for all database-related entities, making the application easier to understand and extend.