from flask import g

from app.db import query_all, execute_sql


def find_all_todo():
    sql = "SELECT * FROM todos WHERE user_id = %s"
    params = (g.current_user_id,)
    return query_all(sql, params)

def find_user(username):
    sql = "SELECT * FROM users WHERE username = %s"
    params = (username,)
    return query_all(sql, params)

def add_user(username,password):
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    params = (username, password)
    return execute_sql(sql, params)

def add_todo(title):
    sql = "INSERT INTO todos (user_id,title, completed) VALUES (%s, %s, %s)"
    params = (g.current_user_id,title,0)
    return execute_sql(sql, params)

def update_todo(fields, values):
    sql = f"UPDATE todos SET {', '.join(fields)} WHERE id = %s and user_id = %s"
    return execute_sql(sql, values)

def delete_todo(id):
    sql = "DELETE FROM todos WHERE id = %s and user_id = %s"
    params = (id, g.current_user_id)
    return execute_sql(sql, params)

def complete_todo(id):
    sql = "SELECT * FROM todos WHERE id = %s and user_id = %s"
    params = (id, g.current_user_id)
    return query_all(sql, params)