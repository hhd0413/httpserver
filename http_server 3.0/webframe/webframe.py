'''
wenframe
功能:
    负责接收来自http_server的请求 (使用IO多路复用（使用poll）)
    处理请求
    将数据打包成json格式发送给httpserver
'''
import json
from socket import *
from select import *
from settings import *
from urls import *

class WEBframe:
    def __init__(self):
        self.init()

    # 初始化套接字
    def init(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
        self.sockfd.bind(frame_addr)
        self.sockfd.listen(5)

    # 启动函数
    def forever(self):
        p = poll()
        # 注册需要关注的IO事件
        p.register(self.sockfd,POLLIN)
        self.fdmap = {self.sockfd.fileno():self.sockfd}
        # 开始循环监控IO事件
        while True:
            events = p.poll()
            for fd,event in events:
                # 客户端连接
                if fd == self.sockfd.fileno():
                    connfd,addr = self.fdmap[fd].accept()
                    p.register(connfd,POLLIN)
                    # 维护字典
                    self.fdmap[connfd.fileno()] = connfd

                # 处理请求
                elif POLLIN & event:
                    self.do_request(self.fdmap[fd])

    def do_request(self,connfd):
        # data:   httpserver-->webframe  {method:'GET',info:'/'} json格式
        data = connfd.recv(1024).decode()
        request = json.loads(data)
        if request['method'] == 'GET':
            self.handle(request['info'],connfd)

    # 处理请求
    def handle(self,request,connfd):
        # 处理网页
        if request == '/' or request[-5:] == '.html':
            self.get_webpage(request,connfd)
        # 处理其他类请求
        else:
            for url,func in urls:
                if url == request:
                    data = json.dumps({'status':'200','data':func()})
                    break
            else:
                data = json.dumps({'status':'200','data':'sorry..'})

            connfd.send(data.encode())
            connfd.close()

    # 获取网页
    def get_webpage(self,request,connfd):
        if request == '/': filename = DIR + '/index.html'
        else: filename = DIR + request
        try:
            f = open(filename)
        except Exception :
            f = open(DIR + '/404.html')
            text = f.read()
            data = {'status': '404', 'data': text}
        else:
            text = f.read()
            data = {'status':'200','data':text}
        data = json.dumps(data)
        connfd.send(data.encode())
        connfd.close()

if __name__ == '__main__':
    wf = WEBframe()
    wf.forever()

































