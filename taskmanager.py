import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

"""
This program will manage a list of tasks using a Firestore database.
"""

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/google_service_api_key.json"

    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'taskmanager-eb178',
    })

    # Get reference to database
    db = firestore.client()
    return db

def get_tasks(db, category=None, status=None):
    """
    Get a list of tasks filtered by category and status
    """
    # Build query
    query = db.collection("tasks")
    # Add optional filters
    if category is not None:
        query = query.where("category", "==", category)
    if status is not None:
        query = query.where("status", "==", status)
    # Execute query
    results = query.stream()
    tasks = []
    # Populate the list array with each task put
    # into a dictionary format.  The ID from the database
    # is added to the dictionary for later use.
    for result in results:
        task = result.to_dict()
        task["id"] = result.id
        tasks.append(task)
    return tasks

def convert_status(status):
    """
    Conver the boolean status to a Open/Closed string
    """
    if status:
        return "Open"
    return "Closed"

def display_tasks(tasks):
    """
    Display tasks in a formatted table.  The ID
    is based on the size of the table and starts at 1.
    """
    print("{:>3}   {:>10}   {:>8}   {}".format("ID", "Category", "Status", "Description"))
    print("{:>3}   {:>10}   {:>8}   {}".format("-"*3, "-"*10, "-"*8, "-"*30))
    num = 1
    for task in tasks:
        print("{:>3}   {:>10}   {:>8}   {}".format(num, task["category"], convert_status(task["status"]), task["description"]))
        num += 1

def insert_task(db, category, description):
    """
    Insert a new task into the datbase.
    """
    task = {"category" : category, "description" : description, "status": True}
    db.collection("tasks").document().set(task)

def delete_task(db, task):
    """
    Delete a task from the database.
    """
    db.collection("tasks").document(task["id"]).delete()

def update_task(db, task, category, description):
    """
    Update a task in the database (category and description)
    """
    ref = db.collection("tasks").document(task["id"])
    ref.update({"category" : category})
    ref.update({"description" : description})

def update_status(db, task, status):
    """
    Update the status of a task into the database
    """
    ref = db.collection("tasks").document(task["id"])
    ref.update({"status" : status})

# Main Program
db = initialize_firestore()
exit_program = False  
# Start the program by showing open tasks in all categories
status = True
category = None
# When redisplay is True, then the updated table will display
# after the command is processed.
redisplay = True
while not exit_program:
    try:
        print()
        # Redisplay the updated table
        if redisplay:
            tasks = get_tasks(db, category, status)
            display_tasks(tasks)
            print()
        else:
            redisplay = True
        # Get the command from the user and split up by commas
        command = input("> ")
        params = command.split(",")
        # Perform the action based on the first parameter
        if params[0] == "h" and len(params) == 1:
            print("q,<o|c|a>,<category|*> - query (o=open, c=closed, a=all)")
            print("c,<id> - close")
            print("o,<id> - re-open")
            print("i,<category>,<description> - insert")
            print("d,<id> - delete")
            print("u,<id>,<category>,<description> - update")
            print("h - help")
            print("x - exit")
            redisplay = False
        elif params[0] == "q" and len(params) == 3:
            # Determine the status and category parameters
            if params[1] == "o":
                status = True
            elif params[1] == "c":
                status = False
            else:
                status = None
            if params[2] == "*":
                category = None
            else:
                category = params[2]
        elif params[0] == "c" and len(params) == 2:
            update_status(db, tasks[int(params[1])-1], False)
        elif params[0] == "o" and len(params) == 2:
            update_status(db, tasks[int(params[1])-1], True)
        elif params[0] == "i" and len(params) == 3:
            insert_task(db, params[1], params[2])
        elif params[0] == "d" and len(params) == 2:
            # Need to be careful about converting id to 0 based index
            delete_task(db, tasks[int(params[1])-1])
        elif params[0] == "u" and len(params) == 4:
            # Need to be careful about converting id to 0 based index
            update_task(db, tasks[int(params[1])-1], params[2], params[3])
        elif params[0] == "x" and len(params) == 1:
            exit_program = True
        else:
            print("Invalid command.")
    except:
        # If number conversions or invalid ID's occur, then catch them 
        # to prevent the program from exiting.
        print("Invalid command.")
