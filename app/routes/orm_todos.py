from flask import Blueprint, jsonify, request, g
from sqlalchemy import text

from app.models import Todo
from app.orm_db import db
from app.utils.auth import auth_required

todo_bp = Blueprint("todo", __name__)
todo_bp.before_request(auth_required)

@todo_bp.route("/todos", methods=["GET"])
def list_todos():
    # 1. 取参数并校验（复用第 3 课校验思路）
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 10, type=int)
    if page < 1 or not 1 <= size <= 100:
        return jsonify({"error": "page/size 参数不合法", "code": 400}), 400

    # 2. 动态拼筛选条件
    q = Todo.query.filter_by(user_id=g.current_user_id)
    completed = request.args.get("completed", type=int)   # 不传 = 不过滤
    if completed in (0, 1):
        q = q.filter_by(completed=bool(completed))

    # 3. 排序白名单：字段名绝不直接吃用户输入
    SORTABLE = {"created_at": Todo.created_at, "id": Todo.id}
    sort_key = request.args.get("sort", "created_at")
    column = SORTABLE.get(sort_key, Todo.created_at)
    q = q.order_by(column.desc() if request.args.get("order") == "desc" else column.asc())

    # 4. 分页并返回标准结构
    pagination = q.paginate(page=page, per_page=size, error_out=False)
    return jsonify({
        "items": [{"id": t.id, "title": t.title, "completed": t.completed}
                 for t in pagination.items],
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages
    })

@todo_bp.route("/todos", methods=["POST"])
def add_todo():
    title = request.json.get("title")
    db.session.add(Todo(title=title, completed=False,user_id=g.current_user_id))
    db.session.commit()
    return jsonify({"message": '添加成功'})

@todo_bp.route("/todos/<int:id>", methods=["PUT"])
def change_todo(id):
    data = request.get_json(silent=True) or {}
    print(data)
    todo = Todo.query.filter_by(id=id).first()
    if "title" in data:
        todo.title = data.get("title")
        db.session.commit()
    if 'completed' in data:
        todo.completed = data.get("completed")
        db.session.commit()
    return {"message": "更新成功"}

@todo_bp.route("/todos/<int:id>", methods=["DELETE"])
def delete_todos(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return '',204

@todo_bp.route("/todos/stats", methods=["GET"])
def stats():
    task_count = Todo.query.filter_by(user_id=g.current_user_id).count()
    complete_count = Todo.query.filter_by(user_id=g.current_user_id,completed = True).count()
    return jsonify({"task_count": task_count, "complete_count": complete_count, "completed_rate":f"{complete_count / task_count * 100:.2f}"}),200

@todo_bp.route("/todos/hand/<int:op_id>", methods=["GET"])
def hand_todos(op_id):
    q = db.session.execute(text("SELECT * FROM todos WHERE id = :op_id"),{"op_id": op_id})
    print(q.fetchone())
    return jsonify(q.fetchone()[0]),200