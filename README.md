
## CC-Project

### Step 1

```console
pip3 install redis
pip3 install pyshorteners
apt-get update && apt-get install redis
vim /etc/redis/redis.conf
# requirepass 123
python3 main.py
# test:
curl --request POST 192.168.220.132:1111 -d url=hello
curl 192.168.220.132:1111/{response}
```

### step 2

```console
docker pull redis
docker run --name redis -d -p 6379:6379 redis redis-server --requirepass "123"
cd step_2
docker build -t surl .
docker run -it surl
curl --request POST {server_ip}:1111 -d url=hello
curl {server_ip}:1111/{response}
```