import json
from datetime import datetime, timedelta

with open("workouts.json", "r") as f:
    workouts = json.load(f)

def filter_workouts():
    # get 2023 workouts
    filtered_workouts = []
    for workout in workouts:
        date = workout["created_at"]
        date_obj = datetime.fromisoformat(date)
        # filter out unknown, misc, and walking
        if workout["sport_id"] in (-1, 63, 71):
            continue
        # filter out unscored, but keep unscorable
        if workout["score_state"] not in ("SCORED", "UNSCORABLE"):
            continue

        if date_obj.year == 2023:
            filtered_workouts.append(workout)
    return filtered_workouts


wos_2023 = filter_workouts()

num_workouts = len(wos_2023)
print("Number of workouts in 2023:", num_workouts)

# Get average kcal and fill missing values
scored_workouts = [wo for wo in wos_2023 if wo["score_state"] == "SCORED"]

sum_kilojoule = sum(wo["score"]["kilojoule"] for wo in scored_workouts)
average_kilojoule = sum_kilojoule / len(scored_workouts)

# fill missing workouts with average kilojoule
for wo in wos_2023:
    if wo["score_state"] == "UNSCORABLE":
        wo["score"] = {"kilojoule": average_kilojoule}

sum_kilojoule = sum(x["score"]["kilojoule"] for x in wos_2023)
sum_kcal = sum_kilojoule * 0.238846
print(f"Total kcal: {sum_kcal:.2f} kcal")

average_kcal = sum_kcal / num_workouts
print(f"Average kcal: {average_kcal:.2f} kcal")

# Get total and average workout duration
sum_duration = timedelta()

for w in wos_2023:
    start = datetime.fromisoformat(w["start"])
    end = datetime.fromisoformat(w["end"])
    duration = end - start
    sum_duration += duration
# print("Total duration:", sum_duration)

mm, ss = divmod(sum_duration.total_seconds(), 60)
hh, mm = divmod(mm, 60)
hh, mm, ss = int(hh), int(mm), int(ss)

# get rid of microseconds for a cleaner print statement
sum_duration_no_ms = timedelta(days=sum_duration.days, seconds=sum_duration.seconds)
print(f"Total duration: {hh}h {mm}m {ss}s ({sum_duration_no_ms})")

average_duration_seconds = sum_duration.total_seconds() / num_workouts
mm, ss = divmod(average_duration_seconds, 60)
hh, mm = divmod(mm, 60)
hh, mm, ss = int(hh), int(mm), int(ss)
print(f"Average duration: {hh}:{mm}:{ss}")

# Get most common activities
from collections import Counter, defaultdict

SPORT_ID_TO_NAME = {
    0: "Running",
    1: "Bicycle",
    33: "Swimming",
    96: "HIIT",
    71: "MISC",
    43: "Pilates",
    44: "Yoga",
    48: "Functional Fitness",
    52: "Hiking",
    -1: "Unknown Activity",
    63: "Walking",
}

workout_id_counters = defaultdict(int)
for wo in wos_2023:
    workout_id_counters[SPORT_ID_TO_NAME[wo["sport_id"]]] += 1

counter = Counter(workout_id_counters)
print("Top 3 activities:")
for activity, count in counter.most_common(3):
    print(f"{activity}: {count}")
