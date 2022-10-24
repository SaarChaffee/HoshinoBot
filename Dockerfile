FROM python:3.8

WORKDIR /HoshinoBot

ENV PATH="${PATH}:/root/.local/bin"

COPY ./ /HoshinoBot/

RUN /usr/local/bin/python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip install --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple\
  && chmod 777 ./res/msyh.ttc \
  && cp ./res/msyh.ttc /usr/share/fonts/truetype/ \
  && sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
  && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
  && apt update \
  && apt -y install fonts-noto \
  && fc-cache -fv

EXPOSE 9220

VOLUME [ "/HoshinoBot" ]

CMD [ "python3","run.py" ]