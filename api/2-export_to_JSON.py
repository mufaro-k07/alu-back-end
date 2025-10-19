#!/usr/bin/python3
"""
Python script that gathers all employees' TODO lists
and exports them to todo_all_employees.json.
"""

import json
import requests
import sys


def fetch_all_users():
    """Fetch all users from the API."""
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching users: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_user_todos(user_id):
    """Fetch TODOs for a specific user by ID."""
    url = "https://jsonplaceholder.typicode.com/todos"
    params = {'userId': user_id}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching todos for user {user_id}: {e}",
              file=sys.stderr)
        return []


def main():
    """Gather all TODOs and export to JSON."""
    all_users_data = {}

    users = fetch_all_users()

    for user in users:
        user_id = str(user.get("id"))
        username = user.get("username")
        todos = fetch_user_todos(user_id)

        all_users_data[user_id] = [
            {
                "username": username,
                "task": task.get("title"),
                "completed": task.get("completed")
            }
            for task in todos
        ]

    filename = "todo_all_employees.json"
    try:
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(all_users_data, json_file, indent=4)
    except IOError as e:
        print(f"Error writing to file {filename}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
