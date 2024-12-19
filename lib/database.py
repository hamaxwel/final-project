import sqlite3

# Database file path
DATABASE_FILE = "carbon_tracker.db"

# Establish a database connection
def connect_db():
    try:
        return sqlite3.connect(DATABASE_FILE)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Initialize the database and create necessary tables
def init_db():
    conn = connect_db()
    if conn is None:  # Check if the connection failed
        print("Failed to connect to the database. Exiting initialization.")
        return

    try:
        cursor = conn.cursor()

        # Create 'users' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                location TEXT NOT NULL
            )
        """)

        # Create 'activities' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                emission_factor REAL NOT NULL
            )
        """)

        # Create 'emission_logs' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emission_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_id INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                date TEXT NOT NULL,
                emissions REAL NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(activity_id) REFERENCES activities(id) ON DELETE CASCADE
            )
        """)

        conn.commit()  # Commit changes to the database
        print("Database and tables initialized successfully!")
    except sqlite3.Error as e:
        print(f"Error initializing tables: {e}")
    finally:
        conn.close()  # Ensure the connection is closed

# Example to insert sample data into the tables (for testing purposes)
def add_sample_data():
    conn = connect_db()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        # Insert sample users
        cursor.execute("INSERT INTO users (name, email, location) VALUES (?, ?, ?)", 
                       ("Alice", "alice@example.com", "USA"))
        cursor.execute("INSERT INTO users (name, email, location) VALUES (?, ?, ?)", 
                       ("Bob", "bob@example.com", "Canada"))
        conn.commit()

        # Insert sample activities
        cursor.execute("INSERT INTO activities (name, emission_factor) VALUES (?, ?)", 
                       ("Driving", 0.24))
        cursor.execute("INSERT INTO activities (name, emission_factor) VALUES (?, ?)", 
                       ("Flying", 0.18))
        conn.commit()

        # Get user and activity IDs (for logs)
        cursor.execute("SELECT id FROM users WHERE email = 'alice@example.com'")
        user_id_alice = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM users WHERE email = 'bob@example.com'")
        user_id_bob = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM activities WHERE name = 'Driving'")
        activity_id_driving = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM activities WHERE name = 'Flying'")
        activity_id_flying = cursor.fetchone()[0]

        # Insert sample emission logs
        cursor.execute("INSERT INTO emission_logs (user_id, activity_id, duration, date, emissions) VALUES (?, ?, ?, ?, ?)", 
                       (user_id_alice, activity_id_driving, 60, "2024-12-18", 14.4))
        cursor.execute("INSERT INTO emission_logs (user_id, activity_id, duration, date, emissions) VALUES (?, ?, ?, ?, ?)", 
                       (user_id_bob, activity_id_flying, 120, "2024-12-18", 21.6))
        conn.commit()

        print("Sample data added successfully!")

    except sqlite3.Error as e:
        print(f"Error adding sample data: {e}")
    finally:
        conn.close()  # Ensure the connection is closed

# Entry point for testing table creation and adding sample data
if __name__ == "__main__":
    init_db()  # Initialize database and tables
    add_sample_data()  # Add sample data to test
