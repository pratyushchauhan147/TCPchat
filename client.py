import socket
import threading

end = 0
saveHost = {
    'PC': '10.5.76.237',
    'TM': '10.5.78.226'
}

# Choosing Nickname
hostip = input('Enter IP Address: ')
port = int(input('Enter port: '))

nickname = input("Choose your nickname: ")
key = input("Password: ")

if hostip in saveHost:
    hostip = saveHost[hostip]

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hostip, port))

# Listening to Server and Sending Nickname
def receive():
    global end
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            elif message == 'PAS':
                client.send(key.encode('utf-8'))
            elif message == 'KeyNotFound':
                end = 1
                print("Wrong key")
                exit(1)
                break
            else:
                print(message)
        except:
            # Close Connection When Error
            print("Disconnected")
            client.close()
            break

def write():
    global end
    while True:
        inp = input('')
        message = '{}: {}'.format(nickname, inp)
        if inp == '/close':
            client.send('CLOSE'.encode('utf-8'))
            client.close()
            break
        elif inp == '/list':
            client.send('LIST'.encode('utf-8'))
        elif inp == '/listname':
            client.send('LISTNAME'.encode('utf-8'))
        elif end == 1:
            break
        elif inp.startswith('/msg'):
            parts = inp.split(' ', 2)
            if len(parts) == 3:
                recipient, private_message = parts[1], parts[2]
                message = f'PRIVATE {recipient} {nickname}: {private_message}'
                print(f'PRIVATE TO {recipient} : {private_message}')
                client.send(message.encode('utf-8'))
            else:
                print("Invalid private message format. Use /msg <recipient> <message>")
        elif inp.startswith('/hid'):
            parts = inp.split(' ', 1)
            if len(parts) > 1:
                message = 'Anonymous: {}'.format(parts[1])
                client.send(message.encode('utf-8'))
            else:
                print("Message not given")
        else:
            client.send(message.encode('utf-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
