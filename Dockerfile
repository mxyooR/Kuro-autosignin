# 使用官方 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

ENV CRON_SIGNIN='30 9 * * *'
ENV TZ=Asia/Shanghai

# 安装依赖
RUN pip install . --no-cache-dir

# 暴露端口（如果需要）
# EXPOSE 8000



# 运行主程序
CMD ["python", "task_scheduler.py"]
