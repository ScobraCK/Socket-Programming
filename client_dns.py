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

        while True:
            print('\nSelect Mode(Exit: 0, Insert: 1, Delete: 2, Search IP: 3, Search Domain: 4)')
            mode = int(input('Mode: '))

            if mode == 0:
                break
            ip = None
            dname = None

            # input ip
            if mode != 4:  # no need in search dname 
                while not ip:
                    ip = input('IP: ')

            # input dname
            if mode != 3:
                while not dname:
                    dname = input('Domain Name: ')

            request = parse_data(mode, ip=ip, dname=dname)
            s.sendall(request)
            raw_data = s.recv(2048)

            data = read_data(raw_data)

            if (status := data['status']) == 1:
                print('Success')
                if mode == 3 or mode == 4:
                    print(f"IP: {data['data']['ip']}, Domain Name: {data['data']['dname']}")

            elif status == 11:
                print('Failed insert due to duplicate entry')
            elif status == 12:
                print('Failed delete due to incorrect ip or dname')
            elif status == 13:
                print('Failed Insert due to empty search value')
            elif status == 14:  # entry not found
                print('Searched entry was not found')
            else:
                print('Unknown Request')

        s.close()
    input()
