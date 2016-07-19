from table import  table
import socket
import demjson

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#s.connect(('127.0.0.1',9999))
tttabel=table

def get_message(socket):
    s=socket

    buffer=[]
    while True:
        d=s.recv(1024).decode('utf-8')
        if d:
            buffer.append(d)
        else:
            break

    data=''.join(buffer)

    comm,content=data.split('/r/n',1)
    return comm,content


def deal_with(comm,content):
    if comm=='message':
        print(content)
    elif comm=='table':
        tttabel.updata(demjson.decode(content))
    xx=input()
    send_message(s,xx)


def send_message(socket,message):
    s=socket
    s.sendto(message.encode('utf-8'),('127.0.0.1',9999))

def game():
    while True:
        comm,content=get_message(s)
        deal_with(comm,content)
