from schemas.Authentication import UserInDB
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SSL
from psycopg2.extras import DictCursor
# Database configuration
db_config = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
    "sslmode": DB_SSL  # Ensure SSL is enabled
}

def get_user(email: str):
    connection = None
    try:
        # Connect to the database
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor(cursor_factory=DictCursor)
        
        # Execute the query with parameters
        query = "SELECT * FROM users WHERE e_mail = %s"
        cursor.execute(query, (email,))
        
        # Fetch the user
        user = cursor.fetchall()
        if user:
            return UserInDB(**user[0])
        return None
            
    except Exception as e:
        print(f"Database error in get_user: {e}")
        return None
    finally:
        # Clean up resources
        if connection:
            cursor.close()
            connection.close()

def add_user_to_db(email: str, hashed_password: str):
    connection = None
    try:
        # Connect to the database
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        
        # Execute the insert query
        query = """
        INSERT INTO users (e_mail, hashed_password,is_confirmed)
        VALUES (%s, %s,FALSE)
        """
        cursor.execute(query, (email, hashed_password))
        
        # Commit the transaction
        connection.commit()
            
    except Exception as e:
        print(f"Database error in add_user_to_db: {e}")
        if connection:
            connection.rollback()
    finally:
        # Clean up resources
        if connection:
            cursor.close()
            connection.close()