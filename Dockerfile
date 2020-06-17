FROM python:3.8
LABEL maintainer="AzurCrystal"

ARG PUID=1000
ENV PYTHONIOENCODING=utf-8
RUN set -x \ 
        && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
        && echo 'Asia/Shanghai' >/etc/timezone \
        && rm -rf /var/lib/apt/lists/* \
        && apt-get clean \
        && apt-get update \
        && apt-get install git -y --no-install-recommends --no-install-suggests \
        && useradd -u $PUID -m HoshinoBot \
        && su HoshinoBot -c \
        "mkdir -p /home/HoshinoBot \
        && cd /home/HoshinoBot \
        && git clone https://gitee.com/saarchaffee/HoshinoBot.git \
        && { \
        echo '#!/bin/sh'; \
        echo 'cd /home/HoshinoBot/HoshinoBot/'; \
        echo '/usr/local/bin/python -m pip install --upgrade pip';\
        echo 'pip3 install -r /home/HoshinoBot/HoshinoBot/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple';\
        echo 'python3.8 /home/HoshinoBot/HoshinoBot/run.py'; \
        } > /home/HoshinoBot/entry.sh \
        && chmod 755 /home/HoshinoBot/entry.sh \
        && chmod +x /home/HoshinoBot/entry.sh" \
        && pip3 install --no-cache-dir -r /home/HoshinoBot/HoshinoBot/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
        && apt-get clean autoclean \
        && apt-get autoremove -y \
        && rm -rf /var/lib/apt/lists/*

USER HoshinoBot

WORKDIR /home/HoshinoBot

EXPOSE 9222

VOLUME /home/HoshinoBot/HoshinoBot

ENTRYPOINT /home/HoshinoBot/entry.sh
