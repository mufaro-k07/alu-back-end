#!/usr/bin/python3
"""
Python script that exports an employee's TODO list to a JSON file.
"""

import json
import requests
import sys


def fetch_employee_data(employee_id):
    """
    Fetch employee info and their TODO list from the API.

    Args:
        employee_id (int): The ID of the employee to query.

    Returns:
        tuple: (user_info: dict, todos_info: list)
    """
    base_url = "https://jsonplaceholder.typicode.com"
    user_url = f"{base_url}/users/{employee_id}"
    todos_url = f"{base_url}/todos"

    try:
        user_response = requests.get(user_url)
        # Use 'params' argument for cleaner filtering (instead of ?userId=...)
        todos_response = requests.get(todos_url,
                                       params={'userId': employee_id})

        # Raise HTTPError for bad responses (4xx or 5xx)
        user_response.raise_for_status()
        todos_response.raise_for_status()

    except requests.exceptions.RequestException as e:
        # Handle connection errors or bad HTTP status codes
        print(f"Error connecting to API: {e}", file=sys.stderr)
        sys.exit(1)

    user_info = user_response.json()
    todos_info = todos_response.json()

    # Check specifically if the employee ID resulted in a valid user
    if not user_info.get('id'):
        print(f"Error: Employee with ID {employee_id} not found.",
              file=sys.stderr)
        sys.exit(1)

    return user_info, todos_info


def export_to_json(employee_id, username, todos):
    """
    Export all TODO list tasks to a JSON file named '<USER_ID>.json'.

    Args:
        employee_id (int): The ID of the employee (used as the dict key).
        username (str): The employee's username.
        todos (list): List of task dictionaries.
    """
    data = {
        str(employee_id): [
            {
                "task": task.get("title"),
                "completed": task.get("completed"),
                "username": username
            }
            for task in todos
        ]
    }

    filename = f"{employee_id}.json"
    try:
        # Added 'indent=4' for readability, but kept line short
        with open(filename, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=4)
    except IOError as e:
        print(f"Error writing to file {filename}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./2-export_to_JSON.py <employee_id>", file=sys.stderr)
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Error: Employee ID must be an integer.", file=sys.stderr)
        sys.exit(1)

    user_info, todos_info = fetch_employee_data(employee_id)
    username = user_info.get("username")
    export_to_json(employee_id, username, todos_info)
