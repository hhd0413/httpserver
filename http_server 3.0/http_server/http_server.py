'''
httpserver 3.0
功能:
    接收来自浏览器的请求  (使用多线程)
    将内容打包成json格式，发给webframe
    接收来自webframe的消息
    将数据发给浏览器
'''
import re
import sys
from socket import *
from threading import Thread
from config import *
import json

class HTTPserver:
    def __init__(self,host='',port=80):
        self.host = host
        self.port = port
        self.ADDR = (self.host,self.port)
        self.init()

    # 初始化套接字
    def init(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
        self.sockfd.bind(self.ADDR)
        self.sockfd.listen(5)

    # 处理请求
    def handle(self,connfd):
        request = connfd.recv(4096).decode()
        if not request:
            connfd.close()
            sys.exit()
        # print(data)
        # data:   httpserver-->webframe  {method:'GET',info:'/'}
        #         webframe-->httpserver {status:'200',data:'ccccc'}
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        env = re.match(pattern,request).groupdict()
        # 将env以json格式发送给webframe
        response = self.connect_webframe(env)
        if response:
            # 将数据发送给浏览器
            self.do_response(connfd,response)

    # 与webframe交互
    def connect_webframe(self, env):
        s = socket()
        s.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
        s.connect((host_frame,port_frame))

        request = json.dumps(env)
        s.send(request.encode())
        data = s.recv(1024 * 1024 * 10).decode()
        if not data:
            return
        # webframe -->httpserver
        # {status: '200', data: 'ccccc'}
        return json.loads(data)

    # 回发http响应给浏览器
    def do_response(self, connfd,response):
        if response['status'] == '200':
            response_head = 'HTTP/1.1 200 OK\r\n'
            response_head += 'Content-Type: text/html\r\n'
            response_head += '\r\n'
            response = response_head + response['data']
        elif response['status'] == '404':
            response_head = 'HTTP/1.1 404 Not Found\r\n'
            response_head += 'Content-Type: text/html\r\n'
            response_head += '\r\n'
            response = response_head + response['data']
        connfd.send(response.encode())
        connfd.close()

    # 启动函数
    def forever(self):
        while True:
            connfd,addr = self.sockfd.accept()
            t = Thread(target=self.handle,args=(connfd,))

            t.setDaemon(True)
            t.start()

if __name__ == '__main__':
    ht = HTTPserver(HOST,PORT)
    ht.forever()

























