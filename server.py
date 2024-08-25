import socket
import threading

host = '0.0.0.0'
port = 6000

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

def remove(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast('{} left!'.format(nickname).encode('utf-8'))
    nicknames.remove(nickname)

def private_message(sender, recipient, message):
    if recipient in nicknames:
        recipient_index = nicknames.index(recipient)
        recipient_client = clients[recipient_index]
        recipient_client.send(f'PRIVATE : {message}'.encode('utf-8'))
        return True
    else:
        return False

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            decodedMes = message.decode('utf-8')
            
            if message == 'LIST'.encode('utf-8'):
                message = str(clients).encode('utf-8')
                client.send(message)  # Send the list of clients only to the requesting client
                print("Client requested list of clients")
                continue
            if message == 'LISTNAME'.encode('utf-8'):
                message = str(nicknames).encode('utf-8')
                client.send(message)  # Send the list of clients only to the requesting client
                print("Client requested list of clients")
                continue
            if message == 'CLOSE'.encode('utf-8'):
                continue

            if decodedMes.startswith('PRIVATE'):
                parts = decodedMes.split(' ', 2)
                recipient = parts[1]
                private_msg = parts[2]
                sender_nickname = nicknames[clients.index(client)]
                pr = private_message(sender_nickname, recipient, private_msg)
                if not pr:
                    client.send(f'User not found.'.encode('utf-8'))
                else:
                    print("Private Message sent")
                continue

            broadcast(message)
        except:
            # Removing And Closing Clients
            remove(client)
            break

# Receiving / Listening Function
def receive():
    while True:
        client, address = server.accept()

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        client.send('PAS'.encode('utf-8'))
        key = client.recv(1024).decode('utf-8')
        if key != pas:
            client.send('KeyNotFound'.encode('utf-8'))
            remove(client)
            continue
        print("Connected with {}".format(str(address)))
        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server started")
pas = input('Set a connection key: ')
print("Connect Key set..")
receive()
