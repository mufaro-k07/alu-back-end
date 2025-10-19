#!/usr/bin/python3
"""
Python script that gathers all employees' TODO lists
and exports them to todo_all_employees.json.
"""

import json
import requests


def fetch_all_users():
    """Fetch all users from the API."""
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_user_todos(user_id):
    """Fetch TODOs for a specific user by ID."""
    url = f"https://jsonplaceholder.typicode.com/todos?userId={user_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    """Gather all TODOs and export to JSON."""
    all_users_data = {}
    users = fetch_all_users()

    for user in users:
        user_id = str(user.get("id"))
        username = user.get("username")
        todos = fetch_user_todos(user_id)
        all_users_data[user_id] = [
            {"username": username, "task": task.get("title"), "completed": task.get("completed")}
            for task in todos
        ]

    with open("todo_all_employees.json", "w", encoding="utf-8") as json_file:
        json.dump(all_users_data, json_file)


if __name__ == "__main__":
    main()
