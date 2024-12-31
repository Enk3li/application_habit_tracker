from datetime import datetime

DEFAULT_USER = "default_user"

class Habit:
    """
    Habit class to represent a habit with various attributes and methods.
    """

    def __init__(self, id, name, task, periodicity, creation_date=None, completion_date=None, streak=0, created_by=DEFAULT_USER, demoData=False, dbID=None):
        """
        Initialize a Habit instance
        """
        self.id = id
        self.name = name
        self.task = task
        self.periodicity = periodicity
        self.creation_date = creation_date or datetime.now()
        self.completion_date = completion_date
        self.streak = streak
        self.created_by = created_by
        self.demoData = demoData
        self.dbID = dbID

    def get_current_datetime(self):
        """
        Get the current date and time.
        """
        return datetime.now()

    def update_dbID(self, habitID):
        """
        Update the database ID of the habit.
        """
        self.dbID = habitID

    def __str__(self):
        """
        Return a string representation of the Habit instance.
        """

        return (
            f"Habit(id={self.id}, name={self.name}, task={self.task}, "
            f"periodicity={self.periodicity}, creation_date={self.creation_date}, "
            f"completion_date={self.completion_date}, streak={self.streak}, "
            f"created_by={self.created_by}, demoData={self.demoData}, dbID={self.dbID})"
        )
