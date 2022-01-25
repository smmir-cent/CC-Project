FROM alpine
RUN apk update
RUN apk add curl && apk add python3 && apk add py3-pip &&  pip3 install requests && pip3 install pyyaml && pip3 install redis && pip3 install pyshorteners
COPY . .
CMD python3 main.py
# docker build -t surl .

# docker pull redis
# docker run --name redis -d -p 6379:6379 redis redis-server --requirepass "123"