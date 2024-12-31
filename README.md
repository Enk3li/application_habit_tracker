 # Habit Tracker Application

## Introduction

The Habit Tracker Application is a Python-based backend system designed to help users define, track, and analyze their habits. The application allows users to create habits with specified periodicities (daily and weekly), track their completion, and gain insights into their habit streaks and performance.

This project was part of my portfolio for the Object-Oriented and Functional Programming with Python Course at the IU International University of Applied Sciences.

## Installation

To install and set up the Habit Tracker Application, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Enk3li/application_habit_tracker.git

   
2. **Set Up a Virtual Environment**:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**:
   pip install -r requirements.txt
   
4. **Initialize the Database**:
    python setup_db.py

### Prerequisites
- Python 3.7 or later
- SQLite3
- Click library
- Questionary
- Pytest (for testing)

## Usage
The Habit Tracker Application provides a command-line interface (CLI) for users to interact with the application. The CLI allows users to perform various tasks related to habit tracking, such as adding new habits, marking habits as completed, updating habits, removing habits, and analyzing habit data.

### Running the Application:
To start the application, run the following command:
python main.py main

### User Choices:
Add a new habit: User can add a new habit by specifying the habit's name, task, periodicity, and creation date.
Mark habit as completed: User can mark a habit as completed by selecting the habit name. This command updates the habit's completion status and records the event in the database.
Update habit: User can update an existing habit by selecting the habit name and modifying its details. In this initial implementation, the update functionality is limited to modifying the habit task.
Remove habit: User can remove a habit and all the related data by selecting the habit name.
List all habits: User can view a list of all currently tracked habits that are stored in the database.
List habits by periodicity: User can view habits in the database filtered by their periodicity (daily or weekly).
Longest streak (all habits): User can see the habit with the longest streak across all tracked habits.
Longest streak (single habit): User can view the longest streak for a specific habit by selecting the habit name.
Load demo data: This command is useful for testing and demonstrating the application's features without manual data entry.
Exit: Exit the application.

## Testing
The Habit Tracker Application includes a comprehensive unit test suite using the pytest framework. The test suite covers database initialization, Create-Read-Update-Delete (CRUD) operations, and analytics functions.

### Running Tests:
pytest

### Test Cases and Predefined Habit Data:
Database Initialization and Preloading: Verify that the database is correctly initialized and preloaded with demo data. Ensure tables are created properly and demo habits and events are inserted without errors.
CRUD Operations: Example tests include adding a new habit, updating an existing habit, and deleting a habit along with its associated events.
Analytics Functions: Validate that analytics functions return correct data, such as retrieving all habits, habits by periodicity, and calculating the longest streaks.
Demo Habits: Include 5 predefined habits with example tracking data for a period of 4 weeks. Cover various tasks and periodicities (daily and weekly) to provide a comprehensive test set. Examples: "Painting" (daily), "Reading" (daily), "Meditation" (weekly), "Cooking" (daily), "Journaling" (weekly).

## Note
This Habit Tracker Application was developed as part of the Object-Oriented and Functional Programming with Python Course at the IU International University of Applied Sciences. The application aims to provide a robust backend for tracking and analyzing user habits, with a focus on modularity, maintainability, and user-friendly interaction via the command-line interface.

