import sqlite3
from datetime import datetime
from habit import Habit
from habitevent import HabitEvent

class HabitTracker:
    """
    HabitTracker class to manage habits and habit events in a database.
    """
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def is_connected(self):
        """
        Check if the database connection is established.
        """
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='habits'")
            return True
        except sqlite3.Error:
            return False

    def add_habit(self, habit):
        """
        Add a new habit to the database.
        """
        with self.conn:
            self.cursor.execute('''INSERT INTO habits (id, name, task, periodicity, creation_date, completion_date, streak, created_by, demoData)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (habit.id, habit.name, habit.task, habit.periodicity, habit.creation_date.strftime("%Y-%m-%d"),
                                 habit.completion_date.strftime("%Y-%m-%d") if habit.completion_date else None, habit.streak, habit.created_by, habit.demoData))
            habit.update_dbID(self.cursor.lastrowid)
            self.conn.commit()

    def add_habit_event(self, habit_event):
        """
        Add a new habit event to the database.
        """
        with self.conn:
            self.cursor.execute('''INSERT INTO habit_events (habitID, date, isInPeriod)
                                   VALUES (?, ?, ?)''',
                                (habit_event.habitID, habit_event.eventDate.strftime("%Y-%m-%d"), habit_event.isInPeriod))
            self.conn.commit()

    def save_habit(self, habit):
        if habit.id is None:
            self.add_habit(habit)
        else:
            self.update_habit(habit)

    def update_habit(self, habit):
        """
        Update an existing habit in the database.
        """
        with self.conn:
            self.cursor.execute('''UPDATE habits
                                   SET task = ?
                                   WHERE name = ?''',
                                (habit.task, habit.name))
            self.conn.commit()

    def remove_habit(self, habit_name):
        """
        Remove a habit and its associated events from the database.
        """
        with self.conn:
            self.cursor.execute('DELETE FROM habits WHERE name=?', (habit_name,))
            self.cursor.execute('DELETE FROM habit_events WHERE habitId IN (SELECT id FROM habits WHERE name=?)', (habit_name,))
            self.conn.commit()

    def mark_habit_completed(self, habit_name):
        """
        Mark a habit as completed and add a habit event.
        """
        with self.conn:
            self.cursor.execute('SELECT id, name, task, periodicity, creation_date, completion_date, streak, created_by, demoData FROM habits WHERE name=?', (habit_name,))
            habit_data = self.cursor.fetchone()
            if not habit_data:
                return None

            habit = Habit(
                id=habit_data[0],
                name=habit_data[1],
                task=habit_data[2],
                periodicity=habit_data[3],
                creation_date=datetime.strptime(habit_data[4], "%Y-%m-%d"),
                completion_date=datetime.strptime(habit_data[5], "%Y-%m-%d") if habit_data[5] else None,
                streak=habit_data[6],
                created_by=habit_data[7],
                demoData=habit_data[8]
            )
            self.add_habit_event(HabitEvent(habitID=habit.id, eventDate=datetime.now()))
            return habit

    def get_habit_events(self, habit_id):
        """
        Fetches all habit events for a given habit ID from the database.

        Args:
          habit_id (int): The ID of the habit for which to retrieve events.

        Returns:
          list: A list of HabitEvent objects or None if no events found.
        """
        self.cursor.execute('''SELECT * FROM habit_events WHERE habitId = ?''', (habit_id,))
        habit_events_data = self.cursor.fetchall()
        habit_events = []
        for row in habit_events_data:
            habit_event = HabitEvent(
                habitID=row[1],
                eventDate=datetime.strptime(row[2], "%Y-%m-%d"),
                isInPeriod=row[3],
                demoData=row[4]
            )
            habit_events.append(habit_event)
        return habit_events
