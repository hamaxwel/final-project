import sqlite3

# Establish a connection to the database
def connect_db():
    try:
        return sqlite3.connect("carbon_tracker.db")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to log an emission
def log_emission(user_id, activity_id, duration, date, emissions):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emission_logs (user_id, activity_id, duration, date, emissions) VALUES (?, ?, ?, ?, ?)",
            (user_id, activity_id, duration, date, emissions)
        )
        conn.commit()
        cursor.execute(
            "SELECT id, user_id, activity_id, duration, date, emissions FROM emission_logs WHERE user_id=?",
            (user_id,)
        )
        return cursor.fetchone()
    except sqlite3.IntegrityError as e:
        print(f"Integrity error logging emission: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error logging emission: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error logging emission: {e}")
    finally:
        conn.close()  # Close the connection

# Function to update an emission
def update_emission(emission_log_id, emissions=None, duration=None):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        if emissions:
            cursor.execute(
                "UPDATE emission_logs SET emissions=? WHERE id=?",
                (emissions, emission_log_id)
            )
        if duration:
            cursor.execute(
                "UPDATE emission_logs SET duration=? WHERE id=?",
                (duration, emission_log_id)
            )
        conn.commit()
        cursor.execute(
            "SELECT id, user_id, activity_id, duration, date, emissions FROM emission_logs WHERE id=?",
            (emission_log_id,)
        )
        return cursor.fetchone()
    except sqlite3.IntegrityError as e:
        print(f"Integrity error updating emission: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error updating emission: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error updating emission: {e}")
    finally:
        conn.close()  # Close the connection

# Function to delete an emission
def delete_emission(emission_log_id):
    conn = connect_db()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM emission_logs WHERE id=?",
            (emission_log_id,)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Integrity error deleting emission: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error deleting emission: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error deleting emission: {e}")
        return False
    finally:
        conn.close()  # Close the connection
