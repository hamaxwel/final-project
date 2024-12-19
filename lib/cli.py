import os
import sqlite3
import click

# Initialize the SQLite database
def init_db():
    """Initialize the database and tables."""
    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )""")
    
    # Create activities table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        emission_factor REAL NOT NULL
    )""")
    
    # Create emission logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emission_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        activity_id INTEGER,
        duration REAL,
        date TEXT,
        emissions REAL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (activity_id) REFERENCES activities(id)
    )""")

    conn.commit()
    conn.close()

# Function to create a new user
@click.command()
def create_user():
    """Create a new user."""
    click.echo("Enter user name: ")
    name = input()
    click.echo("Enter user email: ")
    email = input()

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

    click.echo(f"User '{name}' with email {email} created.")

# Function to update an existing user
@click.command()
def update_user():
    """Update an existing user."""
    click.echo("Enter user ID to update: ")
    user_id = int(input())
    click.echo("Enter new name (leave blank to keep current): ")
    name = input()
    click.echo("Enter new email (leave blank to keep current): ")
    email = input()

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    if name:
        cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
    if email:
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))

    conn.commit()
    conn.close()

    click.echo(f"User {user_id} updated.")

# Function to delete a user
@click.command()
def delete_user():
    """Delete a user."""
    click.echo("Enter user ID to delete: ")
    user_id = int(input())

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    click.echo(f"User {user_id} deleted.")

# Function to view all users
@click.command()
def view_users():
    """View all users."""
    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    for user in users:
        click.echo(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

    conn.close()

# Function to create a new activity
@click.command()
def create_activity():
    """Create a new activity."""
    click.echo("Enter activity name: ")
    name = input()
    click.echo("Enter emission factor: ")
    emission_factor = float(input())

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO activities (name, emission_factor) VALUES (?, ?)", (name, emission_factor))
    conn.commit()
    conn.close()

    click.echo(f"Activity '{name}' with emission factor {emission_factor} created.")

# Function to update an activity
@click.command()
def update_activity():
    """Update an existing activity."""
    click.echo("Enter activity ID to update: ")
    activity_id = int(input())
    click.echo("Enter new name (leave blank to keep current): ")
    name = input()
    click.echo("Enter new emission factor (leave blank to keep current): ")
    emission_factor = input()

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    if name:
        cursor.execute("UPDATE activities SET name = ? WHERE id = ?", (name, activity_id))
    if emission_factor:
        cursor.execute("UPDATE activities SET emission_factor = ? WHERE id = ?", (emission_factor, activity_id))

    conn.commit()
    conn.close()

    click.echo(f"Activity {activity_id} updated.")

# Function to delete an activity
@click.command()
def delete_activity():
    """Delete an activity."""
    click.echo("Enter activity ID to delete: ")
    activity_id = int(input())

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
    conn.commit()
    conn.close()

    click.echo(f"Activity {activity_id} deleted.")

# Function to log a new emission record
@click.command()
def log_emission():
    """Log a new emission record."""
    click.echo("Enter user ID: ")
    user_id = int(input())
    click.echo("Enter activity ID: ")
    activity_id = int(input())
    click.echo("Enter duration: ")
    duration = float(input())
    click.echo("Enter date (YYYY-MM-DD): ")
    date = input()
    click.echo("Enter emissions: ")
    emissions = float(input())

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO emission_logs (user_id, activity_id, duration, date, emissions) VALUES (?, ?, ?, ?, ?)",
                   (user_id, activity_id, duration, date, emissions))
    conn.commit()
    conn.close()

    click.echo(f"Emission logged for user {user_id} with activity {activity_id}.")

# Function to update an emission log
@click.command()
def update_emission():
    """Update an emission log."""
    click.echo("Enter emission log ID to update: ")
    emission_log_id = int(input())
    click.echo("Enter new duration (leave blank to keep current): ")
    duration = input()
    click.echo("Enter new emissions (leave blank to keep current): ")
    emissions = input()

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    if duration:
        cursor.execute("UPDATE emission_logs SET duration = ? WHERE id = ?", (duration, emission_log_id))
    if emissions:
        cursor.execute("UPDATE emission_logs SET emissions = ? WHERE id = ?", (emissions, emission_log_id))

    conn.commit()
    conn.close()

    click.echo(f"Emission log {emission_log_id} updated.")

# Function to delete an emission log
@click.command()
def delete_emission():
    """Delete an emission log."""
    click.echo("Enter emission log ID to delete: ")
    emission_log_id = int(input())

    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM emission_logs WHERE id = ?", (emission_log_id,))
    conn.commit()
    conn.close()

    click.echo(f"Emission log {emission_log_id} deleted.")

# Function to view all emission logs
@click.command()
def view_emission_logs():
    """View all emission logs."""
    conn = sqlite3.connect("carbontrack.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emission_logs")
    emission_logs = cursor.fetchall()

    for log in emission_logs:
        click.echo(f"ID: {log[0]}, User ID: {log[1]}, Activity ID: {log[2]}, Duration: {log[3]}, Date: {log[4]}, Emissions: {log[5]}")

    conn.close()

# Main function to display the interactive menu
def main_menu():
    init_db()  # Initialize the database if not already done

    while True:
        print("==== CarbonTrack CLI ====")
        print("1. Create User")
        print("2. View Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Create Activity")
        print("6. View Activities")
        print("7. Update Activity")
        print("8. Delete Activity")
        print("9. Log Emission")
        print("10. View Emission Logs")
        print("11. Update Emission Log")
        print("12. Delete Emission Log")
        print("13. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_user()  # Calling the function for creating user
        elif choice == "2":
            view_users()  # Calling the function to view users
        elif choice == "3":
            update_user()  # Calling the function to update a user
        elif choice == "4":
            delete_user()  # Calling the function to delete a user
        elif choice == "5":
            create_activity()  # Calling the function for creating activity
        elif choice == "6":
            view_activities()  # Calling the function to view activities
        elif choice == "7":
            update_activity()  # Calling the function to update an activity
        elif choice == "8":
            delete_activity()  # Calling the function to delete an activity
        elif choice == "9":
            log_emission()  # Calling the function to log emission
        elif choice == "10":
            view_emission_logs()  # Calling the function to view emission logs
        elif choice == "11":
            update_emission()  # Calling the function to update an emission log
        elif choice == "12":
            delete_emission()  # Calling the function to delete an emission log
        elif choice == "13":
            print("Exiting...")
            break  # Exit the loop and the program
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
