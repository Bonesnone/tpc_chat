from socket import *
import threading

def send_message():
    while True:
        message = input()
        clientSocket.send(message.encode())

def receive_message():
    while True:
        ServerReply = clientSocket.recv(2048)
        print(ServerReply.decode())

# fixed addr for now
serverName = "127.0.0.1"
serverPort = 10553
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Start two threads: one for sending messages and one for receiving messages
t1 = threading.Thread(target=send_message)
t2 = threading.Thread(target=receive_message)
t1.start()
t2.start()

# Wait for both threads to finish before closing the socket
t1.join()
t2.join()
clientSocket.close()
