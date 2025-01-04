# Beeroomie Backend

Beeroomie Backend is a RESTful web service designed to manage room-sharing functionalities. The project is built using Python's FastAPI framework and follows a modular architecture with well-organized layers for routers, services, and database operations. The backend supports functionalities such as user management, room listings, and booking operations.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Contributing](#contributing)
8. [License](#license)

## Project Overview
Beeroomie Backend aims to streamline room-sharing processes by providing APIs for managing users, rooms, bookings, and more. The backend ensures a secure and scalable solution to meet the needs of modern room-sharing platforms.

## Features
- User registration and authentication
- Room listing management
- Favorite and offer to an advertisement
- Comparing advertisements
- CRUD operations for users, rooms, and bookings
- Database integration with PostgreSQL

## Technologies Used
- **Python**: Programming language used to develop the backend.
- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for database interactions.
- **PostgreSQL**: Database used to store application data.
- **Pydantic**: Data validation and serialization.
- **Alembic**: Database migrations.

## Installation
Follow these steps to set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CharmBat/beeroomie-backend.git
   cd beeroomie-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

## Usage
Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure
```
beeroomie-backend/
├── main.py               # Application entry point
├── config.py             # Configuration file
├── crud/                 # CRUD operations
├── db/                   # Database connections
├── models/               # Database models
├── routers/              # API route definitions
├── schemas/              # Pydantic schemas
├── services/             # Business logic services
├── tests/                # Test cases
├── utils/                # Utility functions
├── requirements.txt      # Project dependencies
├── docker-compose.yml    # Docker configuration
├── init.sql              # Initial database script
└── README.md             # Project documentation
```

## Contributing
Contributions are welcome! Please follow the guidelines below:
1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

