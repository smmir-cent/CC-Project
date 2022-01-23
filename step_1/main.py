from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import requests
import socket
import time
import yaml
import redis
import pyshorteners
import urllib.parse

host_name = "0.0.0.0"
server_port = 8080
expire_time = 120
redis_ip = "127.0.0.1"
redis_passwd = ""
redis_connection = None
shortener = pyshorteners.Shortener()

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        value = redis_connection.get("https://tinyurl.com"+self.path).decode("utf-8") 
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({f'{self.path}': value},indent=4),"utf-8"))
        self.wfile.write(bytes("\n*************\n", "utf-8"))


    def do_POST(self):

        print("**********")
        print(self.path)
        print("**********")

        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        print(content_length)
        print(post_data.decode('utf-8'))
        print(str(self.headers))
        self.send_response(200)
        print("**********")
        postData = urllib.parse.parse_qs(post_data.decode('utf-8'))
        print(postData)
        ## todo parse data
        # shortener.tinyurl.short(data)
        print("**********")

        # self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))



if __name__ == "__main__":  
    if os.path.exists('/src/config.yml'):
        with open("/src/config.yml", 'r') as f:
            config = yaml.safe_load(f)
            print(f'port = {config["port"]}  expire_time = {config["expire_time"]} redis_ip = {config["redis_ip"]} redis_passwd = {config["redis_passwd"]}')
            server_port = config["port"]
            expire_time = config["expire_time"]
            redis_ip = config["redis_ip"]
            redis_passwd = config["redis_passwd"]
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
# curl --request POST 192.168.220.132:1111 --form 'u="hello-yay"'
###########################################################
###########################################################
###########################################################