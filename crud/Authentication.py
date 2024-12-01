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


def confirm_user(userid:str):
    connection=None
    try:
    
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor(cursor_factory=DictCursor)
        query = "UPDATE users SET is_confirmed = true WHERE userid = %s"
        cursor.execute(query, (userid,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"User with userid {userid} confirmed successfully.")
        else:
            print(f"No user found with userid {userid} or the user is already confirmed.")
        
    except Exception as e:
        print(f"Database error in confirm_user: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete_user(userid:str):
    connection=None
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor(cursor_factory=DictCursor)
        query = "DELETE FROM users WHERE userid = %s"
        cursor.execute(query, (userid,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"User with userid {userid} deleted successfully.")
        else:
            print(f"No user found with userid {userid} or the user is already deleted.")
        
    except Exception as e:
        print(f"Database error in delete_user: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()

def update_user_password(userid: str, hashed_password: str):
    connection = None
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor(cursor_factory=DictCursor)
        query = "UPDATE users SET hashed_password = %s WHERE userid = %s"
        cursor.execute(query, (hashed_password, userid))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Password for user with userid {userid} updated successfully.")
        else:
            print(f"No user found with userid {userid} or the user is already deleted.")
    except Exception as e:
        print(f"Database error in update_user_password: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()