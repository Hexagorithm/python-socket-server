#!/usr/bin/python3

import sys
import socket
import threading

PORT = 5050 #server runs here
SERVERIP = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVERIP, PORT)
MESSHEADER = 64 #fixed byte length of message header
MESSFORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(ADDRESS)

def startServer():
    print(f"[S]Listening on {SERVERIP}:{PORT} ...")
    server_socket.listen() # enable connection
    while True:
        client_socket, client_addr = server_socket.accept()
        send("[S]:Connected succesfully!",client_socket)
        thread = threading.Thread(target=clientHandling, args=(client_socket,client_addr),daemon=True)
        thread.start()
        print(f"[S]Online connections: {threading.active_count() - 1}")



def clientHandling(client_socket,client_addr):
    print(f"[+]{client_addr[0]}:{client_addr[1]}")
    is_connected = True
    
    while is_connected:
        message = receive(client_socket)
        print(f"[M][{client_addr[0]}]:\'{message}\'") 
        if message != DISCONNECT_MESSAGE:
            send(message, client_socket)
         
        if message == DISCONNECT_MESSAGE:
            print(f"[-][{client_addr[0]}]")
            is_connected = False
        elif message == None:
            print(f"[client_addr[0]] connection message registered!")
    client_socket.close()
   
    return None

def receive(client_socket):
    message_length = client_socket.recv(MESSHEADER).decode(MESSFORMAT) #length of message
    if message_length == "":
        return None
    message = client_socket.recv(int(message_length)).decode(MESSFORMAT)
    return message

def send(message, client_socket):
    message = message.encode(MESSFORMAT)
    length = str(len(message)).encode(MESSFORMAT) + b' ' * (MESSHEADER - len(str(len(message)).encode(MESSFORMAT)))
    client_socket.send(length)
    client_socket.send(message)
    return None

try:
    startServer()
except KeyboardInterrupt:
    #implement looping through every client socket and close it
    #when a thread is active, the server won't close propelly
    print("Server closed manually!")
    sys.exit()
