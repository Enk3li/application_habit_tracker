from habit import Habit
from habitevent import HabitEvent
from habit_tracker import HabitTracker
from datetime import datetime

# Define date format as a constant
DATE_FORMAT = "%Y-%m-%d"

class Analytics:
    """
    Analytics class to perform various operations on habits.
    """
    def __init__(self, habit_tracker):
        """
        Initialize Analytics with a HabitTracker instance.
        """
        self.habit_tracker = habit_tracker

    def get_all_habits(self):
        """
        Fetch all habits from the database.

        Returns:
            list: A list of Habit objects.
        """
        try:
            self.habit_tracker.cursor.execute("SELECT * FROM habits")
            habit_rows = self.habit_tracker.cursor.fetchall()
            return [self._create_habit_from_row(row) for row in habit_rows]
        except Exception as e:
            # Handle exception (e.g., log the error, re-raise, etc.)
            print(f"Error fetching habits: {e}")
            return []

    def get_habit_by_name(self, habit_name):
        """
        Fetch a habit by its name from the database.

        Args:
            habit_name (str): The name of the habit to retrieve.

        Returns:
            Habit: The Habit object if found, otherwise None.
        """
        try:
            self.habit_tracker.cursor.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
            habit_row = self.habit_tracker.cursor.fetchone()
            return self._create_habit_from_row(habit_row) if habit_row else None
        except Exception as e:
            # Handle exception (e.g., log the error, re-raise, etc.)
            print(f"Error fetching habit by name: {e}")
            return None

    def get_habits_by_periodicity(self, periodicity):
        """
        Fetch habits by their periodicity from the database.

        Args:
            periodicity (str): The periodicity of the habits to retrieve.

        Returns:
            list: A list of Habit objects with the specified periodicity.
        """
        habits = self.get_all_habits()
        return [habit for habit in habits if habit.periodicity == periodicity]

    def get_longest_streak_all(self):
        """
        Get the habit with the longest streak and the length of the streak.

        Returns:
            tuple: A tuple containing the Habit object with the longest streak and the length of the streak.
        """
        habits = self.get_all_habits()
        if not habits:
            return None, 0

        longest_streak_habit = None
        longest_streak = 0
        for habit in habits:
            habit_events = self.habit_tracker.get_habit_events(habit.id)
            if habit_events:
                streak = self.get_longest_streak_habit(habit, habit_events)
                if streak > longest_streak:
                    longest_streak_habit = habit
                    longest_streak = streak

        return longest_streak_habit, longest_streak

    def get_longest_streak_habit(self, habit, habit_events=None):
        """
        Get the longest streak for a given habit.

        Args:
            habit (Habit): The Habit object to calculate the streak for.
            habit_events (list): A list of HabitEvent objects for the habit.

        Returns:
            int: The length of the longest streak.
        """
        if habit_events is None:
            habit_events = self.habit_tracker.get_habit_events(habit.id)

        if not habit_events:
            return 0

        sorted_events = sorted(habit_events, key=lambda event: event.eventDate)
        current_streak = 1
        max_streak = 1

        for i in range(1, len(sorted_events)):
            prev_event, curr_event = sorted_events[i - 1], sorted_events[i]

            if curr_event.is_in_period(habit, curr_event.eventDate):
                current_streak += 1
            else:
                current_streak = 1

            max_streak = max(max_streak, current_streak)

        return max_streak

    def get_demo_tracking(self):
        """
        Fetch all demo habits and their events from the database.

        Returns:
            list: A list of tuples containing Habit objects and their corresponding HabitEvent objects.
        """
        try:
            self.habit_tracker.cursor.execute("SELECT * FROM habits WHERE demoData = 1")
            demo_habit_rows = self.habit_tracker.cursor.fetchall()
            demo_habits_with_events = []
            for row in demo_habit_rows:
                habit = self._create_habit_from_row(row)
                habit_events = self.habit_tracker.get_habit_events(habit.id)
                demo_habits_with_events.append((habit, habit_events))
            return demo_habits_with_events
        except Exception as e:
            # Handle exception (e.g., log the error, re-raise, etc.)
            print(f"Error fetching demo habits: {e}")
            return []

    def _create_habit_from_row(self, row):
        """
        Create a Habit object from a database row.

        Args:
            row (tuple): A tuple containing the habit data from the database.

        Returns:
            Habit: The created Habit object.
        """
        return Habit(
            id=row[0],
            name=row[1],
            task=row[2],
            periodicity=row[3],
            creation_date=datetime.strptime(row[4], DATE_FORMAT),
            completion_date=datetime.strptime(row[5], DATE_FORMAT) if row[5] else None,
            streak=row[6],
            created_by=row[7],
            demoData=row[8]
        )
