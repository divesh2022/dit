import pyodbc

def connect_to_database():
    try:
        connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=smss;"
            "Trusted_Connection=yes;"
    )
        conn = pyodbc.connect(connection_string)
        print("✅ Connection successful!")
        return conn
    except Exception as e:
        print("❌ Connection failed:", e)
        return None
connect_to_database()