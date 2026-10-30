# ① 基础镜像：自带 Python 3.12 的精简版 Linux（slim = 瘦身版，省几百 MB）
FROM python:3.12-slim

# ② 容器内的工作目录：之后的命令都在 /app 下执行
WORKDIR /app

# ③ 先只拷贝依赖清单（这步几乎不变，命中缓存，秒过）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ④ 再拷贝全部业务代码（经常变，放后面，只重建这一层）
COPY . .

# ⑤ 声明端口 + 启动命令
EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["python", "run.py"]