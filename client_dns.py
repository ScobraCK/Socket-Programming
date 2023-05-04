import socket
from dns import *

host = 'localhost'
port = 12000

if __name__ == "__main__":
    host_input = input('Enter server IP (Leave empty for localhost): ')  # for non-local IP connections
    if host_input:
        host = host_input

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print('Connected to server')

        request = parse_data(1, 'A', ip='1.1.1.1', dname='server.test')
        s.sendall(request)
        raw_data = s.recv(2048)
        print(f"Received from server: {read_data(raw_data)}")
        s.close()
    input()