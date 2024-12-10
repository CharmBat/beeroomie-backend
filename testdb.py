from sqlalchemy import inspect
from db import engine, get_db

def test_list_tables():
    """
    Test to list all tables in the database and verify database connection.
    """
    # Create an inspector to interact with the database
    inspector = inspect(engine)
    
    # Get the list of tables
    tables = inspector.get_table_names()
    print("Tables in the database:", tables)
    assert tables is not None, "Failed to retrieve tables. Check your database connection or configuration."
    assert len(tables) > 0, "No tables found in the database. Verify your database schema."

    # Test the database session
    try:
        with get_db() as db:
            assert db is not None, "Failed to create a database session."
            print("Database session created successfully.")
    except Exception as e:
        print("Error during session creation:", e)
        raise AssertionError("Database session test failed.")

# Run the test
if __name__ == "__main__":
    test_list_tables()
