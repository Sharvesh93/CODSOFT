import json
import os
TASK_FILE = "tasks.json"

def load_tasks():
    try:
        if not os.path.exists(TASK_FILE):
            return {}

        with open(TASK_FILE, "r") as file:
            data = json.load(file)

            if not isinstance(data, dict):
                return {}

            return data

    except json.JSONDecodeError:
        print("tasks.json is corrupted. Starting with an empty task list.")
        return {}

    except Exception as e:
        print(f"Error loading tasks: {e}")
        return {}

def save_tasks(tasks):
    try:
        with open(TASK_FILE, "w") as file:
            json.dump(tasks, file, indent=4)

    except Exception as e:
        print(f"Error saving tasks: {e}")

def sort_tasks_by_priority(tasks):
    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    return dict(
        sorted(
            tasks.items(),
            key=lambda item: priority_order.get(
                item[1].get("priority", "Low"),
                4
            )
        )
    )

def update_task_ids(tasks):
    updated_tasks = {}

    for new_id, (_, task) in enumerate(tasks.items(), start=1):
        updated_tasks[str(new_id)] = task

    return updated_tasks

class TodoApp:

    def __init__(self):
        self.tasks = load_tasks()

        if self.tasks:
            self.next_id = max(map(int, self.tasks.keys())) + 1
        else:
            self.next_id = 1

    def view_tasks(self):

        self.tasks = load_tasks()

        if not self.tasks:
            print("\nNo tasks available.")
            return

        print("\nTasks:")
        print("-" * 80)

        for task_id, task in self.tasks.items():

            if not isinstance(task, dict):
                continue

            print(
                f"ID: {task_id} | "
                f"Description: {task.get('description', 'N/A')} | "
                f"Priority: {task.get('priority', 'N/A')} | "
                f"Status: {task.get('status', 'N/A')}"
            )

    def add_task(self, description, priority):

        description = description.strip()

        if not description:
            print("Task description cannot be empty.")
            return

        valid_priorities = ["High", "Medium", "Low"]

        if priority not in valid_priorities:
            print("Priority must be High, Medium, or Low.")
            return

        self.tasks = load_tasks()

        if self.tasks:
            self.next_id = max(map(int, self.tasks.keys())) + 1
        else:
            self.next_id = 1

        self.tasks[str(self.next_id)] = {
            "description": description,
            "priority": priority,
            "status": "Not yet"
        }

        save_tasks(self.tasks)

        print("Task added successfully.")

    def change_priority(self, task_id, new_priority):

        task_id = str(task_id)

        valid_priorities = ["High", "Medium", "Low"]

        if new_priority not in valid_priorities:
            print("Priority must be High, Medium, or Low.")
            return

        self.tasks = load_tasks()

        if task_id not in self.tasks:
            print("Task ID not found.")
            return

        self.tasks[task_id]["priority"] = new_priority

        self.tasks = sort_tasks_by_priority(self.tasks)

        save_tasks(self.tasks)

        print("Priority updated successfully.")

    def delete_task(self, task_id):

        task_id = str(task_id)

        self.tasks = load_tasks()

        if task_id not in self.tasks:
            print("Task ID not found.")
            return

        del self.tasks[task_id]

        self.tasks = update_task_ids(self.tasks)

        save_tasks(self.tasks)

        print("Task deleted successfully.")

    def update_status(self, task_id, status):

        task_id = str(task_id)

        valid_status = ["Done", "Not yet"]

        if status not in valid_status:
            print("Status must be 'Done' or 'Not yet'.")
            return

        self.tasks = load_tasks()

        if task_id not in self.tasks:
            print("Task ID not found.")
            return

        self.tasks[task_id]["status"] = status

        save_tasks(self.tasks)

        print("Status updated successfully.")

    def run(self):

        while True:
            print("\n===== TO-DO LIST =====")
            print("1. View Tasks")
            print("2. Add Task")
            print("3. Change Priority")
            print("4. Delete Task")
            print("5. Update Status")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":

                self.view_tasks()

            elif choice == "2":

                description = input("Enter task description: ")

                print("\nPriority Options:")
                print("High")
                print("Medium")
                print("Low")

                priority = input("Enter priority: ").title()

                self.add_task(description, priority)
                os.system("clear")
                print("Task added successfully.")

            elif choice == "3":

                try:
                    task_id = int(input("Enter task ID: "))
                    new_priority = input(
                        "Enter new priority (High/Medium/Low): "
                    ).title()

                    self.change_priority(task_id, new_priority)

                except ValueError:
                    print("Please enter a valid numeric task ID.")
                os.system("clear")
                print("Priority updated successfully.")
                
            elif choice == "4":

                try:
                    task_id = int(input("Enter task ID: "))
                    self.delete_task(task_id)

                except ValueError:
                    print("Please enter a valid numeric task ID.")
                os.system("clear")
                print("Task deleted successfully.")

            elif choice == "5":

                try:
                    task_id = int(input("Enter task ID: "))

                    print("\nStatus Options:")
                    print("Done")
                    print("Not yet")

                    status = input("Enter status: ").title()

                    if status == "Not Yet":
                        status = "Not yet"

                    self.update_status(task_id, status)

                except ValueError:
                    print("Please enter a valid numeric task ID.")
                os.system("clear")
                print("Status updated successfully.")
                
            elif choice == "6":

                print("Exiting application.")
                os.system("clear")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = TodoApp()
    app.run()