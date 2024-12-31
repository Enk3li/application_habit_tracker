# Define constants for error codes
HABIT_NOT_FOUND = 1
DB_CONNECTION_ERROR = 2
INVALID_PERIODICITY = 3
INVALID_HABIT_NAME = 4

class ErrorHandler:
    """
    ErrorHandler class to manage and display error messages based on error codes.
    """
    # Store error messages as class attributes
    ERROR_MESSAGES = {
        HABIT_NOT_FOUND: "Habit not found",
        DB_CONNECTION_ERROR: "Database connection error",
        INVALID_PERIODICITY: "Invalid periodicity (must be 'daily' or 'weekly')",
        INVALID_HABIT_NAME: "Invalid habit name"
    }

    def __init__(self, error_id):
        self.error_id = error_id

    def get_error_message(self):
        """
        Get the error message based on the error ID.
        """
        return self.ERROR_MESSAGES.get(self.error_id, "Unknown error")

    def handle_error(self):
        """
        Handle the error by printing the error message.
        """
        print(self.get_error_message())
