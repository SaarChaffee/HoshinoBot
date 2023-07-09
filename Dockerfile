FROM python:3.8-slim

WORKDIR /HoshinoBot

ENV PATH="${PATH}:/root/.local/bin"

COPY ./ /HoshinoBot/

RUN python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip install --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
  && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo 'Asia/Shanghai' > /etc/timezone \
  && sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \
  && sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \
  && apt update \
  && apt -y install git fontconfig fonts-noto \
  && chmod 777 ./res/msyh.ttc \
  && cp ./res/msyh.ttc /usr/share/fonts/truetype/ \
  && fc-cache -fv \
  && git config --global http.proxy http://host.docker.internal:7890 \
  && git config --global https.proxy http://host.docker.internal:7890

EXPOSE 9220

VOLUME [ "/HoshinoBot" ]

CMD [ "python3","run.py" ]