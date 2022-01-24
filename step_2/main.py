from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import requests
import socket
import time
import yaml
import redis
import pyshorteners
from datetime import timedelta


host_name = "0.0.0.0"
server_port = 8080
expire_time = 120
redis_ip = "127.0.0.1"
redis_passwd = ""
redis_connection = None
shortener = pyshorteners.Shortener()

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
        print("#######################################################")
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        print(content_length)
        data = post_data.decode('utf-8')
        key_ = "url="
        tiny_url = "https://tinyurl.com/"
        if data.find(key_) == -1:
            # not validate data
            pass 
        else:
            url = data[len(key_):]
            shorted_url = shortener.tinyurl.short(url)
            print(shorted_url)
            redis_connection.setex(shorted_url,timedelta(seconds=expire_time),value=url)
            self.send_response(200)
            self.wfile.write(bytes(f'Requested shorted_url: this_server_ip:{server_port}/{shorted_url[len(tiny_url):]}',"utf-8"))
        print("#######################################################")


if __name__ == "__main__":  
    if os.path.exists('config.yml'):
        with open("config.yml", 'r') as f:
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
# curl --request POST 192.168.220.132:1111 -d url=hello
# curl --request POST 172.17.0.2:1111 -d url=hello
###########################################################
###########################################################
###########################################################