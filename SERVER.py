from socket import *
import threading

clients = []

def handle_client(connectCl1Socket, addr):
    clients.append(connectCl1Socket)
    while True:
        # if the client disconnects, or the message is greater
        #.. than 2048 bytes (buffer size), break loop
        try:
            message = connectCl1Socket.recv(2048)
            msg_char = "message with {} characters recieved".format(
                len(message))
            print(msg_char)
        except:
            break
        # Broadcast the message to all connected clients
        for client in clients:
            # client.send to everyone but himself
            if(client != connectCl1Socket):
                client.send(message)
            # but still send a receipt to sender
            elif(client == connectCl1Socket):
                client.send(msg_char.encode())
                # largely unnecessary, but part of scope
                client.send(str(message).upper().encode())
                
    clients.remove(connectCl1Socket)
    connectCl1Socket.close()
    print("Connection with client", addr, "closed")

serverPort = 10553
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# listen(x), where 'x' should equal servers threads to..
#.. dedicate. Ideally, multiple clients are distributed..
#.. amongst threads. My PC is a 12c/24t machine.
serverSocket.listen(12)
print("The server is listening")

while True:
    connectCl1Socket, addr = serverSocket.accept()
    print("Connection established with client", addr)
    # each client should have its own thread to handle msgs
    t = threading.Thread(target=handle_client, args=(connectCl1Socket, addr))
    t.start()
