from dbutils.pooled_db import PooledDB
from flask import current_app
import pymysql


def init_pool(app):
    cfg = app.config
    app.extensions['db_pool'] = PooledDB(
        creator=pymysql,
        maxconnections=10,
        mincached=2,
        maxcached=5,
        blocking=True,
        ping=1,
        host=cfg["DB_HOST"],
        port=int(cfg["DB_PORT"]),
        user=cfg["DB_USER"],
        password=cfg["DB_PASSWORD"],
        database=cfg["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

def get_conn():
      return current_app.extensions["db_pool"].connection()

def query_all(sql, params=None):
    """查询多条，返回字典列表"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()

def execute_sql(sql, params=None):
    """执行增删改，返回影响行数"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            rows = cur.execute(sql, params)
            conn.commit()      # 写操作必须提交
            return rows
    finally:
        conn.close()