#!/usr/bin/python3
"""
Python script that returns information about an employee's
TODO list progress using a REST API.
"""

import requests
import sys


def get_employee_todo_progress(employee_id):
    """
    Fetch and display TODO list progress for a given employee.

    Args:
        employee_id (int): The ID of the employee to query.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    user_url = f"{base_url}/users/{employee_id}"
    todos_url = f"{base_url}/users/{employee_id}/todos"

    # Fetch employee information and todos
    try:
        user_response = requests.get(user_url)
        todos_response = requests.get(todos_url)

        user_response.raise_for_status()
        todos_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle connection errors or bad HTTP statuses (e.g., 404)
        print(f"Error fetching data: {e}", file=sys.stderr)
        return

    employee = user_response.json()
    todos = todos_response.json()

    employee_name = employee.get("name")
    total_tasks = len(todos)
    done_tasks = [task for task in todos if task.get("completed")]

    # PEP 8 Fix: Break the long print statement across lines
    print(f"Employee {employee_name} is done with tasks("
          f"{len(done_tasks)}/{total_tasks}):")

    for task in done_tasks:
        # The required format is one tabulation and one space: '\t '
        print(f"\t {task.get('title')}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./0-gather_data_from_an_API.py <employee_id>",
              file=sys.stderr)
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Error: Employee ID must be an integer.", file=sys.stderr)
        sys.exit(1)

    get_employee_todo_progress(employee_id)
