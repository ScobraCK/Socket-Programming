import socket
from dns import *

host = '0.0.0.0'
port = 12000

def check_ip():
    '''check if IP is valid format'''
    pass

def check_domain():
    '''check if domain name is valid format'''
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

                    # connection closed
                    if not raw_data:
                        print(f'Connection closed - {addr}')
                        break

                    # decode read data format
                    data = read_data(raw_data)
                    type = data['data']['type']  # unused
                    ip = data['data']['ip']
                    dname = data['data']['dname']

                    # input validation for potential SQL injections
                    # check_ip()
                    # check_domain()

                    # insert
                    if ((status := data.get('status')) == 1):
                        print('Insert Request: ', end='')
                        try:
                            dns_server.insert_domain(ip, dname)
                            print('Success')
                            conn.sendall(parse_data(1))
                        except sqlite3.IntegrityError:
                            conn.sendall(parse_data(11))  # status: 11 = fail
                            print('Failed')
                    # delete
                    elif (status == 2):
                        print('Delete Request: ', end='')
                        if (dns_server.search_ip(ip) == dname):
                            dns_server.delete_domain(ip, dname)
                            print('Success')
                            conn.sendall(parse_data(2))
                        else:
                            print('Fail')
                            conn.sendall(parse_data(12))
                    # search
                    elif (status == 3):
                        print('Search IP Request: ', end='')
                        if not ip:
                            print('Fail')
                            conn.sendall(parse_data(13))
                        else:
                            if (found_dname := dns_server.search_ip(ip)):
                                print('Success')
                                conn.sendall(parse_data(3, ip=ip, dname=found_dname))
                            else: # found_dname == None
                                print('Failed (Not found)')
                                conn.sendall(parse_data(14))
                    elif (status == 4):
                        print('Search Domain Request: ', end='')
                        if not dname:
                            print('Fail')
                            conn.sendall(parse_data(13))
                        else:
                            if (found_ip := dns_server.search_dname(dname)):
                                print('Success')
                                conn.sendall(parse_data(4, ip=found_ip, dname = dname))
                            else: # found_dname == None
                                print('Failed (Not found)')
                                conn.sendall(parse_data(14))
                    
                    else:
                        print('Unknown Request')
                        conn.sendall(parse_data(20))
                    
            
