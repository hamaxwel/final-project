import sqlite3

# Establish a connection to the database
def connect_db():
    try:
        return sqlite3.connect("carbon_tracker.db")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to log an activity
def log_activity(name, emission_factor):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO activities (name, emission_factor) VALUES (?, ?)",
            (name, emission_factor)
        )
        conn.commit()
        cursor.execute(
            "SELECT id, name, emission_factor FROM activities WHERE name=?",
            (name,)
        )
        return cursor.fetchone()
    except sqlite3.IntegrityError as e:
        print(f"Integrity error logging activity: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error logging activity: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error logging activity: {e}")
    finally:
        conn.close()  # Close the connection

# Function to update an activity
def update_activity(activity_id, name=None, emission_factor=None):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        if name:
            cursor.execute(
                "UPDATE activities SET name=? WHERE id=?",
                (name, activity_id)
            )
        if emission_factor:
            cursor.execute(
                "UPDATE activities SET emission_factor=? WHERE id=?",
                (emission_factor, activity_id)
            )
        conn.commit()
        cursor.execute(
            "SELECT id, name, emission_factor FROM activities WHERE id=?",
            (activity_id,)
        )
        return cursor.fetchone()
    except sqlite3.IntegrityError as e:
        print(f"Integrity error updating activity: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error updating activity: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error updating activity: {e}")
    finally:
        conn.close()  # Close the connection

# Function to delete an activity
def delete_activity(activity_id):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM activities WHERE id=?",
            (activity_id,)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Integrity error deleting activity: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error deleting activity: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error deleting activity: {e}")
        return False
    finally:
        conn.close()  # Close the connection

# Function to fetch an activity by name
def get_activity_by_name(name):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, emission_factor FROM activities WHERE name=?",
            (name,)
        )
        return cursor.fetchone()
    except sqlite3.IntegrityError as e:
        print(f"Integrity error fetching activity by name: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error fetching activity by name: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error fetching activity by name: {e}")
    finally:
        conn.close()  # Close the connection
