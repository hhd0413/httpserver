import json
from socket import *

s = socket()

s.bind(('127.0.0.1',8080))

s.listen(5)

while True:
    c,addr = s.accept()
    data = c.recv(1024)
    data = json.dumps({'status':'200','data':'ccccc'})
    print(data)
    c.send(data.encode())
