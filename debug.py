from models import Session, Activity

session = Session()

activities = [
    Activity(name="Car Travel (Gasoline)", emission_factor=0.24),
    Activity(name="Public Transport", emission_factor=0.05),
    Activity(name="Electricity Usage", emission_factor=0.5),
    Activity(name="Meat Consumption (kg)", emission_factor=27.0),
    Activity(name="Biking/Walking", emission_factor=0.0),
]

session.add_all(activities)
session.commit()
session.close()
print("Sample activities added.")
