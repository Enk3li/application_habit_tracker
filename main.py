import click
import questionary
import sqlite3
from habit import Habit
from habitevent import HabitEvent
from habit_tracker import HabitTracker
from analytics import Analytics
from error_handler import ErrorHandler
from datetime import datetime, timedelta


@click.group()
def cli():
    print("\nWelcome to your Habit Tracker application.")
    pass

@cli.command()
def main():
    """
    Main function to run the Habit Tracker application.
    """
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()

    habit_tracker = HabitTracker(conn, cursor)
    if habit_tracker.is_connected():
        print("Connected to the habit tracker database successfully!")
    else:
        print("Error connecting to the database. Please check setup_db.py")
    analytics = Analytics(habit_tracker)

    while True:
        user_choice = questionary.select(
            "Choose an option:",
            choices=[
                "Add a new habit",
                "Mark habit as completed",
                "Update habit",
                "Remove habit",
                "List all habits",
                "List habits by periodicity",
                "Longest streak (all habits)",
                "Longest streak (single habit)",
                "Load demo data",
                "Exit"
            ]
        ).ask()

        if user_choice == "Add a new habit":
            name = questionary.text("Enter the name of the habit:").ask()
            task = questionary.text("Enter the task associated with the habit:").ask()
            periodicity_options = ["daily", "weekly"]
            periodicity = questionary.select(
                "Choose the habit's periodicity:", choices=periodicity_options
            ).ask()

            if periodicity == "weekly":
                frequency_per_week = questionary.text(
                    "How many times per week?:"
                ).ask()
            creation_date = questionary.text("Creation Date (YYYY-MM-DD): ").ask()
            if creation_date:
                creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
            else:
                creation_date = datetime.now()
            completion_date_choice = questionary.select(
                "Completion date?",
                choices=["Never", "On:", "After x occurrences:"]
            ).ask()
            if completion_date_choice == "Never":
                completion_date = datetime.strptime("2999-12-31", "%Y-%m-%d")
            elif completion_date_choice == "On:":
                completion_date_str = questionary.text("Enter date (YYYY-MM-DD): ").ask()
                if completion_date_str:
                    completion_date = datetime.strptime(completion_date_str, "%Y-%m-%d")
                else:
                    completion_date = datetime.strptime("2999-12-31", "%Y-%m-%d")
            elif completion_date_choice == "After x occurrences:":
                try:
                    num_occurrences = int(questionary.text("Enter number of occurrences: ").ask())
                    if periodicity == "daily":
                        completion_date = creation_date + timedelta(days=num_occurrences)
                    elif periodicity == "weekly":
                        completion_date = creation_date + timedelta(weeks=num_occurrences // int(frequency_per_week))
                except ValueError:
                    click.echo("Invalid input for number of occurrences.")
                    completion_date = datetime.strptime("2999-12-31", "%Y-%m-%d")
            created_by = questionary.text("Created By (optional): ").ask() or ""
            try:
                habit = Habit(
                    id=None,
                    name=name,
                    task=task,
                    periodicity=periodicity,
                    creation_date=creation_date,
                    completion_date=completion_date,
                    streak=0,
                    created_by=created_by,
                    demoData=False
                )
                habit_tracker.save_habit(habit)
                print(f"Habit '{name}' has been added successfully!")
            except ValueError as e:
                if "Invalid periodicity" in str(e):
                    error_handler = ErrorHandler(3)
                    print(error_handler.get_error_message())
                elif "Invalid habit name" in str(e):
                    error_handler = ErrorHandler(4)
                    print(error_handler.get_error_message())
                else:
                    print(f"An unexpected error occurred: {e}")

        elif user_choice == "Mark habit as completed":
            try:
                habit_name = questionary.text("Enter the name of the habit to mark complete:").ask()
                habit = analytics.get_habit_by_name(habit_name)
                if habit:
                   habit_tracker.mark_habit_completed(habit_name)
                   print(f"Habit '{habit_name}' marked as completed!")  
            except ValueError as e:
                error_handler = ErrorHandler(1)
                print(error_handler.get_error_message())

        elif user_choice == "Update habit":
            try:
                habit_name = questionary.text("Enter the name of the habit to update:").ask()
                habit = analytics.get_habit_by_name(habit_name)
                if habit:
                    new_task = questionary.text(f"New task for '{habit_name}': ").ask()
                    habit.task = new_task  # Update the task directly
                    habit_tracker.update_habit(habit)
                    print(f"Habit '{habit_name}' updated!")
            except ValueError as e:
                error_handler = ErrorHandler(1)
                print(error_handler.get_error_message())

        elif user_choice == "Remove habit":
            habit_name = questionary.text("Enter the name of the habit to remove:").ask()
            confirmation = questionary.confirm(
                "Are you sure you want to remove this habit?"
            ).ask()
            if confirmation:
               habit = analytics.get_habit_by_name(habit_name)
               if habit:
                habit_tracker.remove_habit(habit_name)
                print(f"Habit '{habit_name}' has been successfully removed!")
            else:
                print("Habit removal cancelled.")

        elif user_choice == "List all habits":
            all_habits = analytics.get_all_habits()
            if all_habits:
                for habit in all_habits:
                    print(f"- {habit.name}")
            else:
                print("You currently have no habits tracked.")

        elif user_choice == "List habits by periodicity":
            periodicity_options = ["daily", "weekly"]
            chosen_periodicity = questionary.select(
                "Choose the periodicity to list:", periodicity_options
            ).ask()
            habits_by_periodicity = analytics.get_habits_by_periodicity(chosen_periodicity)
            if habits_by_periodicity:
                print(f"Habits with periodicity '{chosen_periodicity}':")
                for habit in habits_by_periodicity:
                    print(f"- {habit.name}")
            else:
                 print(f"No habits found with periodicity '{chosen_periodicity}'.")

            
        elif user_choice == "Longest streak (all habits)":
            longest_streak_habit, max_streak = analytics.get_longest_streak_all()
            if longest_streak_habit:
                print(
                    f"Habit with the longest streak: {longest_streak_habit.name} "
                    f"(streak: {max_streak})"
                )
            else:
                print("No valid streaks found for any habits.")

        elif user_choice == "Longest streak (single habit)":
            habit_name = questionary.text("Enter the name of a specific habit:").ask()
            habit = analytics.get_habit_by_name(habit_name)
            if habit:
                max_streak = analytics.get_longest_streak_habit(habit)
                if max_streak:
                    print(
                        f"Longest streak for '{habit_name}': {max_streak} days"
                    )
                else:
                    print(f"No valid streaks found for '{habit_name}'.")

        elif user_choice == "Load demo data":
            demo_habit_confirmation = questionary.confirm(
                "Would you like to load pre-defined demo habits?"
            ).ask()
            if demo_habit_confirmation:
                demo_habits_with_events = analytics.get_demo_tracking()
                for habit, events in demo_habits_with_events:
                    print(f"Habit: {habit.name}")
                    for event in events:
                        print(f"  Event Date: {event.eventDate}")
                print("Demo habits have been loaded successfully.")

        elif user_choice == "Exit":
            break

    conn.close()

cli.add_command(main)

if __name__ == '__main__':
    cli()
