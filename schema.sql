CREATE DATABASE IF NOT EXISTS todo_app DEFAULT CHARSET utf8mb4;
USE todo_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,   -- UNIQUE：用户名不能重复
    password VARCHAR(255) NOT NULL,             -- 存哈希值，所以 255 长度
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                          -- 归属人：数据隔离的关键字段
    title VARCHAR(200) NOT NULL,
    completed TINYINT(1) DEFAULT 0,               -- 0=未完成 1=已完成
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)   -- 外键约束
);