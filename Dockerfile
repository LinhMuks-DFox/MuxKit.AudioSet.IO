FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

# 安装基本工具
RUN apt-get update -y && apt-get upgrade -y --fix-missing && \
    apt-get install -y --fix-missing \
    build-essential \
    zip unzip curl wget vim tree graphviz \
    tk-dev libffi-dev libssl-dev libgeos-dev \
    zlib1g-dev liblzma-dev libbz2-dev libreadline-dev libsqlite3-dev \
    git && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/local/src/*

# 安装 Python 和 Poetry
RUN apt-get update -y && apt-get install -y python3 python3-pip && \
    pip3 install --upgrade pip setuptools requests && \
    pip3 install poetry autopep8 yt-dlp

RUN apt-get update
RUN apt-get install -y ffmpeg
RUN alias cls=clear

# 设置工作目录
WORKDIR /workspace

# 复制 Poetry 文件并安装依赖
COPY pyproject.toml poetry.lock* ./
RUN poetry install

# 设置 Jupyter Lab
# RUN mkdir -p /workspace/notebooks
# CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

# 设置 TTY 为 true
ENV PYTHONUNBUFFERED=1
ENV TTY=true