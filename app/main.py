from flask import Flask, jsonify, request

app = Flask(__name__)

todos = []


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/todos")
def list_todos():
    return jsonify(todos)


@app.post("/todos")
def add_todo():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(error="title is required"), 400
    todo = {"id": len(todos) + 1, "title": title, "done": False}
    todos.append(todo)
    return jsonify(todo), 201


def test_second_todo_gets_id_2(client):
    client.post("/todos", json={"title": "first"})
    response = client.post("/todos", json={"title": "second"})
    assert response.get_json()["id"] == 2


def test_update_todo(client):
    client.post("/todos", json={"title": "old"})
    response = client.put("/todos/1", json={"title": "new", "done": True})
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "title": "new", "done": True}


def test_delete_todo(client):
    client.post("/todos", json={"title": "temp"})
    assert client.delete("/todos/1").status_code == 204
    assert client.get("/todos/1").status_code == 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)