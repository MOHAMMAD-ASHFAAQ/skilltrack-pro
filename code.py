import json
import os
from datetime import date, datetime, timedelta

DATA_FILE = "study_data.json"


# ==================================
# LOAD DATA
# ==================================
def load_data():

    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}


# ==================================
# SAVE DATA
# ==================================
def save_data(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ==================================
# INIT USER
# ==================================
def init_user(user):

    data = load_data()

    if user not in data:

        data[user] = {
            "profile": {
                "name": "",
                "year": "",
                "branch": "",
                "created": False
            },
            "study": [],
            "coding": [],
            "counter": 0,
            "streak": 0,
            "last_active": str(date.today())
        }

        save_data(data)


# ==================================
# PROFILE
# ==================================
def save_profile(user, name, year, branch):

    init_user(user)

    data = load_data()

    data[user]["profile"] = {
        "name": name,
        "year": year,
        "branch": branch,
        "created": True
    }

    save_data(data)


def get_profile(user):

    data = load_data()

    return data.get(user, {}).get(
        "profile",
        {
            "name": "",
            "year": "",
            "branch": "",
            "created": False
        }
    )


# ==================================
# STREAK SYSTEM
# ==================================
def update_streak(user):

    init_user(user)

    data = load_data()

    today = date.today()

    last_active = datetime.strptime(
        data[user]["last_active"],
        "%Y-%m-%d"
    ).date()

    if last_active == today:
        return

    if last_active == today - timedelta(days=1):
        data[user]["streak"] += 1
    else:
        data[user]["streak"] = 1

    data[user]["last_active"] = str(today)

    save_data(data)


# ==================================
# STAR SYSTEM
# 10 Problems = 1 Star
# ==================================
def calculate_stars(problems):

    return int(problems) // 10


# ==================================
# ADD ENTRY
# ==================================
def add_entry(
    user,
    category,
    topic,
    problems,
    languages=None
):

    init_user(user)

    update_streak(user)

    data = load_data()

    data[user]["counter"] += 1

    if languages is None:
        languages = []

    entry = {
        "id": data[user]["counter"],
        "topic": topic,
        "problems": int(problems),
        "stars": calculate_stars(problems),
        "languages": languages,
        "date": str(date.today())
    }

    if category not in data[user]:
        data[user][category] = []

    data[user][category].append(entry)

    save_data(data)


# ==================================
# GET CATEGORY
# ==================================
def get_category(user, category):

    data = load_data()

    return data.get(user, {}).get(category, [])


# ==================================
# GET ALL ENTRIES
# ==================================
def get_all(user):

    data = load_data()

    study = data.get(user, {}).get("study", [])
    coding = data.get(user, {}).get("coding", [])

    return study + coding


# ==================================
# DELETE ENTRY
# ==================================
def delete_entry(user, category, entry_id):

    data = load_data()

    if user not in data:
        return

    data[user][category] = [
        entry
        for entry in data[user][category]
        if entry["id"] != entry_id
    ]

    save_data(data)


# ==================================
# LEADERBOARD
# ==================================
def leaderboard():

    data = load_data()

    board = []

    for username, info in data.items():

        study = info.get("study", [])
        coding = info.get("coding", [])

        total_problems = (
            sum(i["problems"] for i in study)
            +
            sum(i["problems"] for i in coding)
        )

        total_stars = (
            sum(i.get("stars", 0) for i in study)
            +
            sum(i.get("stars", 0) for i in coding)
        )

        board.append(
            {
                "user": username,
                "name": info["profile"]["name"],
                "streak": info["streak"],
                "stars": total_stars,
                "problems": total_problems
            }
        )

    board.sort(
        key=lambda x: (
            x["stars"],
            x["problems"]
        ),
        reverse=True
    )

    return board


# ==================================
# RAW DATA
# ==================================
def load_raw():

    return load_data()
