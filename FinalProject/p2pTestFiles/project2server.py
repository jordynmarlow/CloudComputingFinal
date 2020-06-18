#:/usr/bin/python3


def charcount(file):
	count=0
	for char in file:
		if not char.isspace():
			count = count + 1
	return count

def wordcount(file):
	words = file.split()
	count = 0
	for word in words:
		if not word.isspace():
			count = count + 1
	return count

def linecount(file):
	lines = file.split("\n")
	count = 0
	for line in lines:
		if line:
			count = count + 1
	return count

def main(file):
	return "Characters: "+str(charcount(file))+"\nWords: "+str(wordcount(file))+"\nLines: "+str(linecount(file))



import socket

MAX_SIZE = 1024

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 9999

serverSocket.bind((host, port))

serverSocket.listen(5)                                           

while True:
   # establish a connection
   clientsocket,addr = serverSocket.accept()      

   print("Got a connection from %s" % str(addr))
   f=clientsocket.recv(1024).decode('utf-8')
   #msg = main(f)
   clientsocket.send(f.encode('utf-8'))
   clientsocket.close()




