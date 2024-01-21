
## Analyze your Whoop workouts with Python

This code can be used to extract all workouts using the Whoop API.

**Credits**: The `whoop.py` file with the Whoop API Client implementation was simply copied from https://github.com/hedgertronic/whoop/.

## Example Output

```console
Number of workouts in 2023: 279
Total kcal: 100562.94 kcal
Average kcal: 360.44 kcal
Total duration: 169h 42m 2s (7 days, 1:42:02)
Average duration: 0:36:29
Top 3 activities:
Running: 164
Functional Fitness: 58
Yoga: 42
```
## Step 1: Installation

```console
pip install -r requirements.txt
```

The only dependencies listed in there are `Authlib` and `requests`.

## Step 2: Get Workouts

Set the following variables in `get_workouts.py`:

- `username`: Your Whoop email/username
- `password`: Your Whoop password
- `start_date`: The day until it should collect the workouts

Then run

```console
python get_workouts.py
```

This will collect the workouts from today until the specified start date and dumps it to a file called `workouts.json`.

## Step 3: Analyze Workouts

Run

```console
python analyze_workouts.py
```

This loads the JSON file and prints the stats for 2023.

**Note**: The current logic filters for 2023 workouts and ignores activities categorized as *Unknown*, *MISC*, and *Walking*. If you want to modify this logic, change the code in the `filter_workouts()` function.

## How to identify the activity from the Whoop `sport_id`

Whoop specifies a `sport_id` for each workout. I compared these numbers with my workouts to identify the corresponding activity.

So far I've converted the following `sport_id` values to workout names:

```python
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
```