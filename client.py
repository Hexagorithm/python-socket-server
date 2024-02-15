#!/usr/bin/python3
import socket
import sys


OPTIONS = {'1','2','3','4'}
PORT = 5050 
SERVERIP = "192.168.33.6"
SERVERADDRESS = (SERVERIP, PORT)
MESSHEADER = 64 
MESSFORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

is_connected = False

    


def showOptions():
    print("\n\n\n\n\n\n\n\n\n")
    print("Options for the connection:")
    print("  1 - connect to server")
    print("  2 - send message to server")
    print("  3 - disconnect from server")
    print("  4 - close program")

def getOption():
    global option
    option = None
    while option not in OPTIONS:
        option = str(input("Input option: "))
        if option not in OPTIONS:
            print("Option invalid!")

def handleOptions(option):
    if option == '1':
        connect()
        connection_message = receive(client_socket)
        print(f"{connection_message}")

    elif option == '2':
        message = str(input("Message:"))
        send_error = send(message)
        if not send_error:
            remessage = receive(client_socket)
            print(f"[S]:{remessage}")

    elif option == '3':
        closeConnection()

    elif option == '4':
        if is_connected:
            closeConnection()
        sys.exit()

    else:
        print("What the fuck?")
        exit()

def send(message):
    if not is_connected:
        print("E:Can\'t send message: user not connected.")
        return 1
    message_encoded = message.encode(MESSFORMAT)
    message_length = len(message)
    message_length_encoded = str(message_length).encode(MESSFORMAT) #we will be sending the lenght as a message too
    message_length_encoded_padded = message_length_encoded + b' '* (MESSHEADER - len(message_length_encoded))#make sure the length is the appropriate header length
    client_socket.send(message_length_encoded_padded)
    client_socket.send(message_encoded)
    return 0 

def receive(client_socket):
    message_length = int(client_socket.recv(MESSHEADER).decode(MESSFORMAT))
    message = client_socket.recv(message_length).decode(MESSFORMAT)
    return message


def connect():
    global client_socket,is_connected
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(SERVERADDRESS) # as opposed to server_socket.bind()
    is_connected = True


def closeConnection():
    global is_connected
    if not is_connected:
        print("E:Can\'t close connection: user not connected")
        return None
    send(DISCONNECT_MESSAGE)

    client_socket.close()
    is_connected = False
    print("Connection closed!")

def main():
    try:
        while True:
            showOptions()
            getOption()
            handleOptions(option)
    except KeyboardInterrupt:
        if is_connected:
            closeConnection()
        print("Program closed manually.") 
        sys.exit()

if __name__ == "__main__":
    main()
