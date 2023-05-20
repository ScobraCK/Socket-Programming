import sqlite3, json
from typing import TypedDict, Optional
from enum import Enum

class DNS():
    def __init__(self) -> None:
        self.con = sqlite3.connect('dns.db')
        self.cur = self.con.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS domains (ip text PRIMARY KEY, dname text UNIQUE)
        """)

    def insert_domain(self, ip: str, dname: str):
        self.cur.execute(f"INSERT INTO domains VALUES (?, ?)", (ip, dname))
        self.con.commit()

    def delete_domain(self, ip: str, dname: str):
        self.cur.execute(f"DELETE FROM domains WHERE ip = ? AND dname = ?", (ip, dname))
        self.con.commit()

    def search_ip(self, ip: str):
        res = self.cur.execute(f"SELECT dname FROM domains WHERE ip=?", (ip,))  # tuple
        data = res.fetchone()
        if data:
            return data[0]
        else:
            return None
    
    def search_dname(self, domain: str):
        res = self.cur.execute(f"SELECT ip FROM domains WHERE dname=?", (domain,))  # tuple
        data = res.fetchone()
        if data:
            return data[0]
        else:
            return None
    
    def close(self):
        self.con.close()

class DataField(TypedDict, total=False):
    type: str  # A, NS, CNAME etc
    ip: str
    dname: str

class MyDNSProtocol(TypedDict):
    '''
    status flag
    Client
    1: insert
    2: delete (matching ip, dname)
    3: search ip
    4: search dname
    

    Server
    1: ok
    
    11: Failed Insert (duplicate data exists)
    12: Failed Delete (non-matching ip,dname)
    13: Failed Search (ip/dname was not given)
    14: Failed Search (not found)

    20: Unknown Request
    '''
    status: int
    data: DataField

def read_data(data):
    json_data = json.loads(data.decode('utf-8'))  # byte string -> dict
    return MyDNSProtocol(json_data)

def parse_data(status: int, type: str='A', ip: str=None, dname: str=None):
    data_field = DataField(type=type, ip=ip, dname=dname)
    payload = MyDNSProtocol(status=status, data=data_field)
    return json.dumps(payload, ensure_ascii=False).encode('utf-8')

def check_db(dns: DNS):
    for row in dns.cur.execute("""SELECT * FROM domains"""):
        print(row)
     

if __name__ == "__main__":
    dns = DNS()
    try:
        pass
        # dns.insert_domain('1.2.3.4', 'test.domain')
        # dns.insert_domain('1.2.3.5', 'test.domain.2')
        # dns.insert_domain('1.2.3.6', 'test.domain.3')
        # dns.insert_domain('1.2.3.7', 'test.domain')
        # domain = dns.search_ip('1.2.3.4')
        # ip = dns.search_dname('test.domain')
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    
    print(dns.search_ip('1.1.1.1'))
    check_db(dns)
    
    # print()
    # print(ip[0])
    # print(domain[0])

    test=parse_data(1, ip='test')
    test_dict = read_data(test)
    print(test_dict['data']['dname'])

    
