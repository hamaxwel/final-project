import sqlite3

# Establish a connection to the database
def connect_db():
    try:
        return sqlite3.connect("carbon_tracker.db")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to create a user
def create_user(name, email, location):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, location) VALUES (?, ?, ?)",
                       (name, email, location))
        conn.commit()
        cursor.execute("SELECT id, name, email, location FROM users WHERE email=?", (email,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        conn.close()  # Close the connection

# Function to update a user
def update_user(user_id, name=None, email=None, location=None):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        if name:
            cursor.execute("UPDATE users SET name=? WHERE id=?", (name, user_id))
        if email:
            cursor.execute("UPDATE users SET email=? WHERE id=?", (email, user_id))
        if location:
            cursor.execute("UPDATE users SET location=? WHERE id=?", (location, user_id))
        conn.commit()
        cursor.execute("SELECT id, name, email, location FROM users WHERE id=?", (user_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error updating user: {e}")
        return None
    finally:
        conn.close()  # Close the connection

# Function to delete a user
def delete_user(user_id):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        conn.close()  # Close the connection

# Function to fetch a user by email
def get_user_by_email(email):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, location FROM users WHERE email=?", (email,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error fetching user by email: {e}")
        return None
    finally:
        conn.close()  # Close the connection
