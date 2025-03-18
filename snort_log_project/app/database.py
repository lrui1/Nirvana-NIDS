import sqlite3
from config import DB_PATH

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS snort3_netlog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seconds INTEGER, action TEXT, class TEXT, dir TEXT,
        dst_addr TEXT, dst_ap TEXT, dst_port INTEGER,
        eth_dst TEXT, eth_len INTEGER, eth_src TEXT, eth_type TEXT,
        gid INTEGER, iface TEXT, ip_id INTEGER, ip_len INTEGER,
        msg TEXT, mpls INTEGER, pkt_gen TEXT, pkt_len INTEGER,
        pkt_num INTEGER, priority INTEGER, proto TEXT, rev INTEGER,
        rule TEXT, service TEXT, sid INTEGER, src_addr TEXT,
        src_ap TEXT, src_port INTEGER, tcp_ack INTEGER, tcp_flags TEXT,
        tcp_len INTEGER, tcp_seq INTEGER, tcp_win INTEGER,
        tos INTEGER, ttl INTEGER, vlan INTEGER, timestamp TEXT,
        b64_data TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS snort3_attlog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seconds INTEGER, action TEXT, class TEXT, dir TEXT,
        dst_addr TEXT, dst_ap TEXT, dst_port INTEGER,
        eth_dst TEXT, eth_len INTEGER, eth_src TEXT, eth_type TEXT,
        gid INTEGER, iface TEXT, ip_id INTEGER, ip_len INTEGER,
        msg TEXT, mpls INTEGER, pkt_gen TEXT, pkt_len INTEGER,
        pkt_num INTEGER, priority INTEGER, proto TEXT, rev INTEGER,
        rule TEXT, service TEXT, sid INTEGER, src_addr TEXT,
        src_ap TEXT, src_port INTEGER, tcp_ack INTEGER, tcp_flags TEXT,
        tcp_len INTEGER, tcp_seq INTEGER, tcp_win INTEGER,
        tos INTEGER, ttl INTEGER, vlan INTEGER, timestamp TEXT,
        b64_data TEXT
    )
    ''')
    conn.commit()
    conn.close()

# 数据插入函数
def insert_data(table, json_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    columns = ', '.join(json_data.keys())
    placeholders = ', '.join(['?'] * len(json_data))
    sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
    cursor.execute(sql, tuple(json_data.values()))
    conn.commit()
    conn.close()
