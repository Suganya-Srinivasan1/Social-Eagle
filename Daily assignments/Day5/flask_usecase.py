from flask import Flask, request, jsonify
#Flask → creates the web application
#request → reads data sent by the client (JSON, params, etc.)
#jsonify → converts Python data (dict/list) into JSON responses
app = Flask(__name__)

# In-memory data store
tasks = []
next_id = 1


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


# Get a single task
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


# Create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.json

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


# Update a task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["completed"] = data.get("completed", task["completed"])
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404


# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    initial_length = len(tasks)
    
    # Filter the list
    tasks = [t for t in tasks if t["id"] != task_id]
    
    # Check if the list actually shrunk
    if len(tasks) == initial_length:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)