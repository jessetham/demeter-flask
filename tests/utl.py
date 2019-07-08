from random import randint
from app import db
from app.models import Category, Reading, Sensor, User

# Global list used for test cases
SENSORS = []
CATEGORIES = []
READINGS = []
READING_UPPER_LIMIT = 100
READING_LOWER_LIMIT = 0
USERS = []


def init():
    global SENSORS
    global CATEGORIES
    global READINGS
    global USERS

    SENSORS = [
        {"name": "abacus", "categories": ["noise", "temperature"]},
        {"name": "bushranger", "categories": ["temperature", "humidity"]},
        {"name": "camrose", "categories": ["humidity", "noise"]},
        {"name": "demascus", "categories": ["brightness", "energy"]},
        {
            "name": "evergreen",
            "categories": ["humidity", "temperature", "noise", "brightness"],
        },
    ]
    CATEGORIES = [
        {"name": "temperature", "units": "C"},
        {"name": "humidity", "units": "RH"},
        {"name": "noise", "units": "dB"},
        {"name": "brightness", "units": "lx"},
        {"name": "energy", "units": "J"},
    ]
    READINGS = []
    USERS = [
        {
            "name": "Jim",
            "password": "super",
            "sensors": ["abacus", "bushranger", "demascus"],
        },
        {
            "name": "Pam",
            "password": "secure",
            "sensors": ["camrose", "evergreen", "bushranger"],
        },
        {"name": "Dwight", "password": "password", "sensors": ["abacus", "demascus"]},
        {"name": "Michael", "password": "that", "sensors": ["abacus", "camrose"]},
        {"name": "Creed", "password": "secures", "sensors": ["evergreen", "demascus"]},
    ]


def add_categories_to_db():
    for category in CATEGORIES:
        c = Category()
        c.from_dict(category)
        db.session.add(c)
        db.session.commit()
        category["id"] = c.id


def add_sensors_to_db():
    for sensor in SENSORS:
        s = Sensor()
        s.from_dict(sensor)
        db.session.add(s)
        db.session.commit()
        sensor["id"] = s.id


def add_readings_to_db():
    for sensor in SENSORS:
        for category in sensor["categories"]:
            reading = {
                "data": randint(READING_LOWER_LIMIT, READING_UPPER_LIMIT),
                "category": category,
                "sensor": sensor["name"],
            }
            r = Reading()
            r.from_dict(reading)
            db.session.add(r)
            db.session.commit()
            reading["id"] = r.id
            READINGS.append(reading)


def add_users_to_db():
    for user in USERS:
        u = User()
        u.from_dict(user)
        db.session.add(u)
        db.session.commit()
        user["id"] = u.id
