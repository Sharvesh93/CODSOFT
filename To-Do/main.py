import json

def sort_tasks_by_priority(tasks):
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    return dict(sorted(tasks.items(), key=lambda item: priority_order.get(item[1]["priority"], 4)))

def update_task_id(tasks): 
    updated_tasks = {}
    new_id = 1
    for task_id in sorted(tasks.keys(), key=int):
        updated_tasks[new_id] = tasks[task_id]
        new_id += 1
    return updated_tasks

class TodoApp:
    
    def __init__(self):
        self.tasks = {}  # Dictionary to store tasks with unique IDs
        self.next_id = 1

    def view_tasks(self):
        try:
            with open('tasks.json', 'r') as file : 
                self.tasks = json.load(file)
            for task_id in self.tasks: 
                task = self.tasks[task_id]
                print(f"Id : {task_id} | Description: {task['description']} | Priority: {task['priority']} | Status: {task['status']}")
        except FileNotFoundError:
            print("No tasks found. Please add a task first.")
        except Exception as e:
            print(f"An error occurred while loading tasks: {e}")


    def add_task(self , task, prior):
        self.tasks[self.next_id] = {"description": task, "priority": prior, "status": "Not yet"}
        self.tasks['priority'] = prior
        self.next_id += 1 
        try:
            with open('tasks.json', 'w') as file:
                json.dump(self.tasks, file)
        except Exception as e:
            print(f"An error occurred while saving the task: {e}")
      
    def priority(self, task_id, new_priority):
        if task_id in self.tasks:
            self.tasks[task_id]["priority"] = new_priority

    def delete_task(self, task_id):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
            if task_id in self.tasks:
                del self.tasks[task_id]
            self.tasks = update_task_id(self.tasks)
        
        except FileNotFoundError:
            print("No tasks found. Please add a task first.")
            return
        except Exception as e:
            print(f"An error occurred while loading tasks: {e}")
            return
            
        try:
            with open('tasks.json', 'w') as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as e:
            print(f"An error occurred while saving the task: {e}")

    def run(self) : 
        while True:
            print("\nTo-Do List Application")
            print("1. View Tasks")
            print("2. Add Task")
            print("3. Change Priority")
            print("4. Update Task")
            print("5. Delete Task")
            print("6. Exit")
            choice = input("Enter your choice: ")
            
            # View tasks 
            if choice == '1':
                self.view_tasks()
            
            # Add task 
            elif choice == '2':
                task_desc = input("Enter task description: ")
                self.add_task(task_desc, None)
                
                print("Task added successfully.")
            
            # Change priority 
            elif choice == '3':
                try:
                    task_id = int(input("Enter task ID to change priority: "))
                    new_priority = input("Enter new priority (High/Medium/Low): ")
                    self.priority(task_id, new_priority)
                    
                    print("Priority changed successfully.")
                except ValueError:
                    print("Invalid input. Please enter a valid task ID.")
            
            # Delete task
            elif choice == '4':
                try:
                    task_id = int(input("Enter task ID to delete: "))
                    self.delete_task(task_id)
                    
                    print("Task deleted successfully.")
                except ValueError:
                    print("Invalid input. Please enter a valid task ID.")
            
            # Update task 
            elif choice == '5':
                pass 
                # To implement the update the task state either done or not done

            # Exit application
            elif choice == '6':
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = TodoApp()
    app.run()

"""

JSON file format will be : 
1) description : string
2) priority : string (High/Medium/Low)
3) status : string (Done/Not yet)

"""