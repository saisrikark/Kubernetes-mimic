FROM alpine:3.7

WORKDIR /acts

COPY . /acts

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --trusted-host pypi.python.org -r requirements.txt && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache && \
    apk add --no-cache git && \
    apk add --no-cache bash && \
    python3 db_creator.py 

EXPOSE 80

ENV TEAM_ID CC_265_307_309_330

CMD ["python3","__init__.py"]

