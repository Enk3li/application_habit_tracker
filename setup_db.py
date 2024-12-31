import sqlite3
from datetime import datetime, timedelta
from habit import Habit
from habitevent import HabitEvent

class Database:
    """
    Database class to manage the creation and preloading of the habits database.
    """
    
    def __init__(self, db_name='habits.db'):
        """
        Initialize the Database with a connection to the specified database file.

        Args:
            db_name (str): The name of the database file.
        """
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """
        Create the habits and habit_events tables if they do not already exist.
        """
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                task TEXT,
                periodicity TEXT,
                creation_date TEXT,
                completion_date TEXT,
                streak INTEGER DEFAULT 0,
                created_by TEXT,
                demoData BOOLEAN NOT NULL DEFAULT 0
            )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS habit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habitId INTEGER NOT NULL,
                date DATE NOT NULL,
                isInPeriod BOOLEAN NOT NULL DEFAULT 0,
                demoData BOOLEAN NOT NULL DEFAULT 0
            )''')

    def demo_habits_with_events(self) -> list:
        """
        Create demo habits and events and return them.

        Returns:
            list: A list of tuples containing Habit objects and their corresponding HabitEvent objects.
        """
        creation_date = datetime(2024, 11, 1)
        completion_date = datetime(2024, 11, 30)
        demo_person_name = "Max Mustermann"

        demo_habits = [
            Habit(id=1, name="Painting", task="Create", periodicity="daily", creation_date=creation_date,
                  completion_date=completion_date, streak=0, created_by=demo_person_name, demoData=True),
            Habit(id=2, name="Reading", task="Relax", periodicity="daily", creation_date=creation_date,
                  completion_date=completion_date, streak=0, created_by=demo_person_name, demoData=True),
            Habit(id=3, name="Meditation", task="Relax", periodicity="weekly", creation_date=creation_date,
                  completion_date=completion_date, streak=0, created_by=demo_person_name, demoData=True),
            Habit(id=4, name="Cooking", task="Create & Eating", periodicity="daily", creation_date=creation_date,
                  completion_date=completion_date, streak=0, created_by=demo_person_name, demoData=True),
            Habit(id=5, name="Journaling", task="To build self-awareness", periodicity="weekly", creation_date=creation_date,
                  completion_date=completion_date, streak=0, created_by=demo_person_name, demoData=True)
        ]

        demo_habit_events_painting = [HabitEvent(habitID=1, eventDate=datetime(2024, 11, day), demoData=True) for day in range(1, 30)]
        demo_habit_events_reading = [HabitEvent(habitID=2, eventDate=datetime(2024, 11, day), demoData=True) for day in range(1, 30, 2)]
        demo_habit_events_meditation = [HabitEvent(habitID=3, eventDate=datetime(2024, 11, 1) + timedelta(weeks=week), demoData=True) for week in range(1, 5)]
        demo_habit_events_cooking = [HabitEvent(habitID=4, eventDate=datetime(2024, 11, day), demoData=True) for day in range(1, 30)]
        demo_habit_events_journaling = [HabitEvent(habitID=5, eventDate=datetime(2024, 11, 1) + timedelta(days=2) + timedelta(weeks=week), demoData=True) for week in range(1, 5)]

        # Calculate and set initial streaks for demo habits 
        for habit in demo_habits:
           if habit == demo_habits[0]:  # Painting
            habit.streak = 29 
           elif habit == demo_habits[1]:  # Reading
            habit.streak = 15
           elif habit == demo_habits[2]:  # Meditation
            habit.streak = 4
           elif habit == demo_habits[3]:  # Cooking
            habit.streak = 29
           elif habit == demo_habits[4]:  # Journaling
            habit.streak = 4 

        # Combine demo habits and their corresponding events into a list of tuples
        demo_habits_with_events = [
            (demo_habits[0], demo_habit_events_painting),
            (demo_habits[1], demo_habit_events_reading),
            (demo_habits[2], demo_habit_events_meditation),
            (demo_habits[3], demo_habit_events_cooking),
            (demo_habits[4], demo_habit_events_journaling)
        ]

        return demo_habits_with_events 

          
    def preload_db(self):
        """
        Preloads the database with predefined demo habits and their corresponding events.
        """
        demo_habits_with_events = self.demo_habits_with_events()
        cursor = self.conn.cursor()
        for habit, habit_events in demo_habits_with_events:
            cursor.execute('''INSERT OR IGNORE INTO habits (id, name, task, periodicity, creation_date, completion_date, streak, created_by, demoData)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (habit.id, habit.name, habit.task, habit.periodicity, habit.creation_date.strftime("%Y-%m-%d"),
                            habit.completion_date.strftime("%Y-%m-%d"), habit.streak, habit.created_by, habit.demoData))
            print(f" - Name: {habit.name}, Task: {habit.task}, Periodicity: {habit.periodicity}, Creation_date: {habit.creation_date.strftime("%Y-%m-%d")}, Completion_date: {habit.completion_date.strftime("%Y-%m-%d")}, Streak:{habit.streak}")
            for habitEvent in habit_events:
                cursor.execute('''INSERT OR IGNORE INTO habit_events (habitID, date, isInPeriod, demoData)
                                  VALUES (?, ?, ?, ?)''',
                               (habitEvent.habitID, habitEvent.eventDate.strftime("%Y-%m-%d"), habitEvent.isInPeriod, habitEvent.demoData))
                print(f"Inserted event for habit: {habit.name} on {habitEvent.eventDate.strftime("%Y-%m-%d")}") 
        self.conn.commit()
        
    

    def close_connection(self):
     
        self.conn.close()


if __name__ == "__main__":
    db = Database()
    db.preload_db()
    db.close_connection()
