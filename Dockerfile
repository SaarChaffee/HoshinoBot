FROM python:3.8-slim

WORKDIR /HoshinoBot

ENV PATH="${PATH}:/root/.local/bin"

COPY ./ /HoshinoBot/

RUN python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip install --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 9220

VOLUME [ "/HoshinoBot" ]

CMD [ "python3","run.py" ]