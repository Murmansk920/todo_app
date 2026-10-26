from flask import Blueprint, jsonify, request, abort, g

from app.service.todos import find_all_todo, add_todo, update_todo, delete_todo, complete_todo
from app.utils.auth import auth_required

todo_bp = Blueprint("todo", __name__)

todo_bp.before_request(auth_required)

@todo_bp.route("/todos")
def todo_list():
    return jsonify([todo for todo in find_all_todo()])

@todo_bp.route("/todos", methods=["POST"])
def add_one_todo():
    title = request.json.get("title")
    added = add_todo(title)
    if added == 1:
        return jsonify({"message": '添加成功'})
    else:
        abort(500)

@todo_bp.route("/todos/<int:id>", methods=["PUT"])
def change_todo(id):
    data = request.get_json(silent=True) or {}
    fields, values = [], []
    for k in ('title', 'completed'):
        if k in data:
            fields.append(f"{k} = %s")
            values.append(data[k])
    if not fields:
        return {"error": "没有可更新的字段"}, 400
    values.append(id)
    values.append(g.current_user_id)
    update_todo(fields, values)
    return {"message": "更新成功"}

@todo_bp.route("/todos/<int:id>", methods=["DELETE"])
def delete_todos(id):
    delete_todo(id)
    return '',204

@todo_bp.route("/todos/<int:id>")
def get_status_todo(id):
    return jsonify(complete_todo(id))

