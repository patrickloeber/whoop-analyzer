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
    -1: "Activity",
    0: "Running",
    1: "Cycling",
    16: "Baseball",
    17: "Basketball",
    18: "Rowing",
    19: "Fencing",
    20: "Field Hockey",
    21: "Football",
    22: "Golf",
    24: "Ice Hockey",
    25: "Lacrosse",
    27: "Rugby",
    28: "Sailing",
    29: "Skiing",
    30: "Soccer",
    31: "Softball",
    32: "Squash",
    33: "Swimming",
    34: "Tennis",
    35: "Track & Field",
    36: "Volleyball",
    37: "Water Polo",
    38: "Wrestling",
    39: "Boxing",
    42: "Dance",
    43: "Pilates",
    44: "Yoga",
    45: "Weightlifting",
    47: "Cross Country Skiing",
    48: "Functional Fitness",
    49: "Duathlon",
    51: "Gymnastics",
    52: "Hiking/Rucking",
    53: "Horseback Riding",
    55: "Kayaking",
    56: "Martial Arts",
    57: "Mountain Biking",
    59: "Powerlifting",
    60: "Rock Climbing",
    61: "Paddleboarding",
    62: "Triathlon",
    63: "Walking",
    64: "Surfing",
    65: "Elliptical",
    66: "Stairmaster",
    70: "Meditation",
    71: "Other",
    73: "Diving",
    74: "Operations - Tactical",
    75: "Operations - Medical",
    76: "Operations - Flying",
    77: "Operations - Water",
    82: "Ultimate",
    83: "Climber",
    84: "Jumping Rope",
    85: "Australian Football",
    86: "Skateboarding",
    87: "Coaching",
    88: "Ice Bath",
    89: "Commuting",
    90: "Gaming",
    91: "Snowboarding",
    92: "Motocross",
    93: "Caddying",
    94: "Obstacle Course Racing",
    95: "Motor Racing",
    96: "HIIT",
    97: "Spin",
    98: "Jiu Jitsu",
    99: "Manual Labor",
    100: "Cricket",
    101: "Pickleball",
    102: "Inline Skating",
    103: "Box Fitness",
    104: "Spikeball",
    105: "Wheelchair Pushing",
    106: "Paddle Tennis",
    107: "Barre",
    108: "Stage Performance",
    109: "High Stress Work",
    110: "Parkour",
    111: "Gaelic Football",
    112: "Hurling/Camogie",
    113: "Circus Arts",
    121: "Massage Therapy",
    123: "Strength Trainer",
    125: "Watching Sports",
    126: "Assault Bike",
    127: "Kickboxing",
    128: "Stretching",
    230: "Table Tennis",
    231: "Badminton",
    232: "Netball",
    233: "Sauna",
    234: "Disc Golf",
    235: "Yard Work",
    236: "Air Compression",
    237: "Percussive Massage",
    238: "Paintball",
    239: "Ice Skating",
    240: "Handball",
    248: "F45 Training",
    249: "Padel",
    250: "Barry's",
    251: "Dedicated Parenting",
    252: "Stroller Walking",
    253: "Stroller Jogging",
    254: "Toddlerwearing",
    255: "Babywearing",
    258: "Barre3",
    259: "Hot Yoga",
    261: "Stadium Steps",
    262: "Polo",
    263: "Musical Performance",
    264: "Kite Boarding",
    266: "Dog Walking",
    267: "Water Skiing",
    268: "Wakeboarding",
    269: "Cooking",
    270: "Cleaning",
    272: "Public Speaking"
}


workout_id_counters = defaultdict(int)
for wo in wos_2023:
    workout_id_counters[SPORT_ID_TO_NAME[wo["sport_id"]]] += 1

counter = Counter(workout_id_counters)
print("Top 3 activities:")
for activity, count in counter.most_common(3):
    print(f"{activity}: {count}")
