from datetime import datetime, timedelta

# Define constants for periodicity values
DAILY = "daily"
WEEKLY = "weekly"

class HabitEvent:
    """
    HabitEvent class to represent an event associated with a habit.
    """
    def __init__(self, habitID, eventDate, isInPeriod=False, demoData=False):
        self.habitID = habitID
        self.eventDate = eventDate
        self.isInPeriod = isInPeriod
        self.demoData = demoData

    def is_in_period(self, habit, current_date):
        """
        Check if the event is within the specified period for the habit.
        """
        if habit.periodicity == DAILY:
            return True
        elif habit.periodicity == WEEKLY:
            return self._is_in_weekly_period(habit, current_date)
        else:
            return False

    def _is_in_weekly_period(self, habit, current_date):
        """
        Helper method to check if the event is within the weekly period.
        """
        time_delta = (current_date - habit.creation_date).days
        weeks_passed = time_delta // 7
        expected_completion_dates = [habit.creation_date + timedelta(weeks=week) for week in range(weeks_passed + 1)]

        for expected_date in expected_completion_dates:
            if expected_date <= self.eventDate <= expected_date + timedelta(days=6):
                return True
        return False
