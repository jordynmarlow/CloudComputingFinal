#:/usr/bin/python3
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
   cThread = threading.Thread(target=self.handler, args=(c, a))
   cThread.daemon = True
   cThread.start()
   self.connections.append(c)
   print("Got a connection from %s" % str(addr))
   f=clientsocket.recv(1024).decode('utf-8')
   clientsocket.send(f.encode('utf-8'))

def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break