from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import socket
import yaml
import redis
from datetime import timedelta
import hashlib
import requests

host_name = "0.0.0.0"
server_port = 8080
expire_time = 120
redis_ip = "127.0.0.1"
redis_passwd = ""
redis_connection = None


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        # requested_url = socket.gethostbyname(socket.gethostname())+":"+str(server_port) + self.path
        requested_url = self.path
        print("requested_url: " + requested_url[5:])
        response = "Not Found ===> first post it !"
        real_requested_url = redis_connection.get(requested_url[5:])
        if real_requested_url != None:
            real_requested_url = real_requested_url.decode("utf-8")
            try:
                response = requests.get(real_requested_url).text
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                response = "url is not valid"
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({f'{requested_url}': response},indent=4),"utf-8"))
        self.wfile.write(bytes("\n", "utf-8"))



    def do_POST(self):

        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        # print(content_length)
        data = post_data.decode('utf-8')
        key_ = "url="
        if data.find(key_) == -1:
            # not validate data
            pass 
        else:
            url = data[len(key_):]
            print("url:", url)
            hash_length = 6
            hash_object = hashlib.sha256(str(url).encode('utf-8'))
            shorted_url = socket.gethostbyname(socket.gethostname())+":"+str(server_port) + "/"
            if hash_length<len(hash_object.hexdigest()):
                hash = hash_object.hexdigest()[:hash_length]
                shorted_url = hash
            else:
                raise Exception("Length too long. Length of {y} when hash length is {x}.".format(x=str(len(hash_object.hexdigest())),y=hash_length))

            print("shorted url:", shorted_url)
            redis_connection.setex(shorted_url,timedelta(seconds=expire_time),value=url)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({f'{url}': shorted_url},indent=4),"utf-8"))
            self.wfile.write(bytes("\n", "utf-8"))


if __name__ == "__main__":  
    if os.path.exists('config.yml'):
        with open("config.yml", 'r') as f:
            config = yaml.safe_load(f)
            print(f'port = {config["port"]}  expire_time = {config["expire_time"]} redis_ip = {config["redis_ip"]}')
            server_port = config["port"]
            expire_time = config["expire_time"]
            redis_ip = config["redis_ip"]
            # redis_passwd = config["redis_passwd"]
            redis_passwd = os.environ.get('REDIS_PASSWORD')
            redis_connection = redis.Redis(host=redis_ip,password=redis_passwd) 
    else:
        print(f'(default) ==> port = {server_port} expire_time = {expire_time} redis_ip = {redis_ip} redis_passwd = {redis_passwd}')


    webServer = HTTPServer((host_name, server_port), MyServer)
    print("******************* "+socket.gethostbyname(socket.gethostname())+":"+str(server_port)+" *******************")

    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")





###########################################################
###########################################################
###########################################################
# pip3 install redis
# pip3 install pyshorteners
# curl 192.168.220.132:1111/hello
# curl --request POST 192.168.220.132:1111 -d url=hello
# curl --request POST 172.17.0.2:1111 -d url=hello


# curl --request POST web-service/api -d url=hello
# curl web-service/api/yay89jj
# minikube kubectl -- attach surl-85fd4cd7f4-dw7tk -i -t
# minikube kubectl -- attach net-utils -c net-utils -i -t


'''
cd /home/user/CloudComputing/CC-Project/step_3/step_2/
docker build -t smahdimir/surl:latest .
docker push smahdimir/surl:latest

cd /home/user/CloudComputing/CC-Project/
minikube kubectl delete -- -f step_3/config-map.yaml
minikube kubectl delete -- -f step_3/web-service.yaml
minikube kubectl delete -- -f step_3/web-deployment.yaml
minikube kubectl delete -- -f step_3/secret.yaml
minikube kubectl delete -- -f step_3/redis-deployment.yaml
minikube kubectl delete -- -f step_3/redis-service.yaml
minikube kubectl delete -- -f step_3/redis-pv.yaml
minikube kubectl delete -- -f step_3/redis-pvc.yaml
minikube kubectl delete -- -f step_3/hpa.yaml
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################

*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
minikube kubectl apply -- -f step_3/config-map.yaml
minikube kubectl apply -- -f step_3/web-deployment.yaml
minikube kubectl apply -- -f step_3/web-service.yaml
minikube kubectl apply -- -f step_3/secret.yaml

minikube kubectl apply -- -f step_3/redis-pv.yaml
minikube kubectl apply -- -f step_3/redis-pvc.yaml

minikube kubectl apply -- -f step_3/redis-deployment.yaml
minikube kubectl apply -- -f step_3/redis-service.yaml

minikube kubectl apply -- -f step_3/hpa.yaml

*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************

*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
minikube kubectl apply -- -f step_3/config-map.yaml
minikube kubectl apply -- -f step_3/web-deployment.yaml
minikube kubectl apply -- -f step_3/web-service.yaml
minikube kubectl apply -- -f step_3/secret.yaml

minikube kubectl apply -- -f step_3/redis-pv.yaml
minikube kubectl apply -- -f step_3/redis-pvc.yaml

minikube kubectl apply -- -f step_3/redis-service.yaml
minikube kubectl apply -- -f step_3/redis-statefulset.yaml

minikube kubectl apply -- -f step_3/hpa.yaml

*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************
*******************************************************************************************************



minikube kubectl get cm
minikube kubectl get deployments.apps
minikube kubectl get secret
minikube kubectl get pods
minikube kubectl get services
minikube kubectl get ep

############# test
minikube kubectl -- attach net-utils -c net-utils -i -t
curl --request POST web-service/api -d url=http://google.com
curl web-service/api/aa2239


kubectl autoscale deployment web-deployment.yaml --cpu-percent=60 --min=2 --max=8

minikube kubectl -- attach surl-85fd4cd7f4-dw7tk -it
'''
###########################################################
###########################################################
###########################################################