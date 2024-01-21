import json
from whoop import WhoopClient

username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

start_date="2022-10-12 23:59:59.999999"

print("Get workouts...")
with WhoopClient(username, password) as client:
    workouts = client.get_workout_collection(start_date=start_date)

with open("workouts.json", "w") as f:
    json.dump(workouts, f, indent=4)

print(f"Found {len(workouts)} workouts and saved it to `workouts.json`")