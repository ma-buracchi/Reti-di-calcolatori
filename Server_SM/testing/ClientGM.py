import socket

with open('TestGM', 'r') as f:
    string = f.readline()
    lines = string.split(',')
    i = 0
    result = ""
    while i < len(lines):
        request = lines[i] + '\r\n'
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 8080))
        client.sendall(request)
        response = client.recv(50)
        result = result + response
        client.close()
        i += 1
    print result
