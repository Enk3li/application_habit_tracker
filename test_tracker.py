import pytest
import sqlite3
from habit import Habit
from habitevent import HabitEvent
from habit_tracker import HabitTracker
from analytics import Analytics
from datetime import datetime, timedelta
from setup_db import Database

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """
    Fixture to set up the database for testing.

    Returns:
        tuple: A tuple containing the database connection and cursor.
    """
    db = Database(db_name=':memory:')
    db.create_tables()
    db.preload_db()
    conn = db.conn
    cursor = conn.cursor()
    yield conn, cursor
    conn.close()

def test_get_all_habits(setup_db):
    """
    Test the get_all_habits method of the Analytics class.
    """
    conn, cursor = setup_db
    tracker = HabitTracker(conn, cursor)
    analytics = Analytics(tracker)
    habits = analytics.get_all_habits()
    assert len(habits) == 5

def test_get_habit_by_name(setup_db):
    """
    Test the get_habit_by_name method of the Analytics class.
    """
    conn, cursor = setup_db
    tracker = HabitTracker(conn, cursor)
    analytics = Analytics(tracker)
    habit = analytics.get_habit_by_name("Painting")
    assert habit.name == "Painting"

def test_get_habits_by_periodicity(setup_db):
    """
    Test the get_habits_by_periodicity method of the Analytics class.
    """
    conn, cursor = setup_db
    tracker = HabitTracker(conn, cursor)
    analytics = Analytics(tracker)
    daily_habits = analytics.get_habits_by_periodicity("daily")
    weekly_habits = analytics.get_habits_by_periodicity("weekly")
    assert len(daily_habits) == 3
    assert len(weekly_habits) == 2

def test_get_longest_streak_all(setup_db):
    """
    Test the get_longest_streak_all method of the Analytics class.
    """
    conn, cursor = setup_db
    tracker = HabitTracker(conn, cursor)
    analytics = Analytics(tracker)
    longest_streak_habit, max_streak = analytics.get_longest_streak_all()
    assert longest_streak_habit.name == "Painting"
    assert max_streak == 29

def test_get_longest_streak_habit(setup_db):
    """
    Test the get_longest_streak_habit method of the Analytics class.
    """
    conn, cursor = setup_db
    tracker = HabitTracker(conn, cursor)
    analytics = Analytics(tracker)
    habit = analytics.get_habit_by_name("Painting")
    max_streak = analytics.get_longest_streak_habit(habit)
    assert max_streak == 29

if __name__ == "__main__":
    pytest.main()
