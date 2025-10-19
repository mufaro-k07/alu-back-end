#!/usr/bin/python3
"""
Python script that exports an employee's TODO list to a CSV file.
"""

import csv
import requests
import sys


def fetch_employee_data(employee_id):
    """
    Fetch employee info and their TODO list from the API.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    user_url = f"{base_url}/users/{employee_id}"
    todos_url = f"{base_url}/todos?userId={employee_id}"

    user_response = requests.get(user_url)
    todos_response = requests.get(todos_url)

    if user_response.status_code != 200:
        print("Error: Employee not found.")
        sys.exit(1)

    user_info = user_response.json()
    todos_info = todos_response.json()

    return user_info, todos_info


def export_to_csv(employee_id, username, todos):
    """
    Export all TODO list tasks to a CSV file named '<USER_ID>.csv'.
    Format: "USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"
    """
    filename = f"{employee_id}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for task in todos:
            writer.writerow([
                employee_id,
                username,
                task.get("completed"),
                task.get("title")
            ])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./1-export_to_CSV.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Error: Employee ID must be an integer.")
        sys.exit(1)

    user_info, todos_info = fetch_employee_data(employee_id)
    username = user_info.get("username")
    export_to_csv(employee_id, username, todos_info)
