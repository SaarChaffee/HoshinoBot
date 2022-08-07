FROM python:3.8

WORKDIR /HoshinoBot

ENV PATH="${PATH}:/root/.local/bin"

COPY ./ /HoshinoBot/

RUN /usr/local/bin/python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip install --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip install Jinja2==3.0.3 -U -i https://pypi.tuna.tsinghua.edu.cn/simple\
  && pip install werkzeug==2.0.3 -U -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 9220

VOLUME [ "/HoshinoBot" ]

CMD [ "python3","run.py" ]