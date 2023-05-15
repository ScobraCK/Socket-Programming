import socket
from dns import *

host = 'localhost'
port = 12000

def check_ip():
    pass

def check_domain():
    pass

if __name__ == "__main__":
    dns_server = DNS()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f'Server listening on port {port}')
        while True:
            conn, addr = s.accept()
            print(f'Connected by {addr} - ', end='')
            with conn:  # context manager to ensure exit
                while True:
                    # recieve data           
                    raw_data = conn.recv(2048)
                    # decode read data format
                    data = read_data(raw_data)

                    # insert
                    if (status := data.get('status') == 1):
                        print('Insert Request: ', end='')

                        # check_ip()
                        # check_domain()
                        try:
                            dns_server.insert_domain(data['data']['ip'], data['data']['dname'])
                            print('Success')
                            conn.sendall(parse_data(1, 'A', data['data']['ip'], data['data']['dname']))
                        except sqlite3.IntegrityError:
                            print('Failed')
                    elif (status := data.get('status') == 2):
                        print('Delete Request: ', end='')

                        try:
                            dns_server.delete_domain(data['data']['ip'], data['data']['dname'])
                            print('Success')
                            conn.sendall(parse_data(2, 'A', data['data']['ip'], data['data']['dname']))
                        except sqlite3.IntegrityError:
                            print('Failed')
                    elif (status := data.get('status') == 3):
                        print('Search IP Request: ', end='')

                        try:
                            dns_server.search_ip(data['data']['ip'])
                            print('Success')
                            conn.sendall(parse_data(3, 'A', data['data']['ip'], data['data']['dname']))
                        except sqlite3.IntegrityError:
                            print('Failed')
                    elif (status := data.get('status') == 4):
                        print('Search Domain Request: ', end='')
                        
                        try:
                            dns_server.search_domain(data['data']['dname'])
                            print('Success')
                            conn.sendall(parse_data(4, 'A', data['data']['ip'], data['data']['dname']))
                        except sqlite3.IntegrityError:
                            print('Failed')
                    break
              
