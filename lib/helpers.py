from models import Session, user, activity, emission_log
from datetime import datetime

# Initialize the database (Create tables if not already created)
def initialize_db():
    from models import Base, engine
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

# Add a new user to the database
def add_user():
    session = Session()
    name = input("Enter the user's name: ")
    location = input("Enter the user's location: ")
    
    new_user = user(name=name, location=location)
    session.add(new_user)
    session.commit()
    print(f"User {name} added successfully.")

# Log an activity (i.e., track CO2 emissions)
def log_activity():
    session = Session()
    
    user_id = int(input("Enter user Vehicle: "))
    activity_name = input("Enter number of vehicles: ")
    emission_factor = float(input("Enter the amount of Fuel (litres per unit): "))
    units = float(input("Enter the number of kilometers: "))
    
    # Check if the user exists
    user = session.query(user).filter(user.id == user_id).first()
    if not user:
        print(f"User with ID {user_id} not found.")
        return

    # Add activity
    activity = activity(name=activity_name, emission_factor=emission_factor)
    session.add(activity)
    session.commit()

    # Log the emission
    emission_log = emission_log(user_id=user_id, activity_id=activity.id, units=units)
    session.add(emission_log)
    session.commit()

    print(f"Activity logged for {user.name}.")

# View all emission logs
def view_logs():
    session = Session()
    logs = session.query(emission_log).all()
    
    if not logs:
        print("No logs found.")
        return

    for log in logs:
        user = session.query(user).filter(user.id == log.user_id).first()
        activity = session.query(activity).filter(activity.id == log.activity_id).first()
        print(f"{user.name} performed {activity.name} ({log.units} units) on {log.timestamp}.")
