import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))

while True:
	record=s.recv(1024).decode('utf-8')
	print(record)
	if record=='请您发言':
		myword=input()
		s.send(myword.encode('utf-8'))

