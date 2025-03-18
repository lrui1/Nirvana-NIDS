import sqlite3

from config import DB_PATH

# 建立连接，获取数据库操作对象
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
class_type = '命令执行攻击'
limit = 10
offset = 0
cursor.execute(
    "SELECT id, class, seconds,b64_data,dst_ap,ip_id,ip_len,msg,proto,rule,sid,src_ap,timestamp FROM snort3_attlog where class = ? LIMIT ? OFFSET ?",
    (class_type, limit, offset))
rows = cursor.fetchall()
cursor.execute("SELECT count(*) as cnt FROM snort3_attlog where class = ?", (class_type,))
totals = cursor.fetchall()
data = [dict(row) for row in rows]
# 关闭连接
conn.close()
print(totals[0]['cnt'])