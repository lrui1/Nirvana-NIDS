from flask import Blueprint, jsonify, request
import sqlite3
from config import DB_PATH

# 创建 Blueprint
attlog = Blueprint('attlog', __name__)


@attlog.route('/attlog/type', methods=['GET'])
def get_type_attlog():
    class_type = str(request.args.get('class', ''))
    print(class_type)
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if class_type != '':
        cursor.execute(
            "SELECT id, class, seconds,b64_data,dst_ap,ip_id,ip_len,msg,proto,rule,sid,src_ap,timestamp FROM snort3_attlog where class = ? ORDER BY id DESC LIMIT ? OFFSET ?",
            (class_type, limit, offset))
        rows = cursor.fetchall()
        cursor.execute("SELECT count(*) as cnt FROM snort3_attlog where class = ?", (class_type,))
        totals = cursor.fetchall()
    else:
        cursor.execute(
            "SELECT id, class, seconds,b64_data,dst_ap,ip_id,ip_len,msg,proto,rule,sid,src_ap,timestamp FROM snort3_attlog ORDER BY id DESC LIMIT ? OFFSET ?",
            (limit, offset))
        rows = cursor.fetchall()
        cursor.execute("SELECT count(*) as cnt FROM snort3_attlog")
        totals = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    response = {
        "total": totals[0]['cnt'],
        "data": data
    }
    return jsonify(response)


# 路由：清空 attlog 数据
@attlog.route('/attlog', methods=['DELETE'])
def clear_netlog():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM snort3_attlog")
    conn.commit()
    conn.close()

    return jsonify({"message": "snort3_netlog table cleared."})


# 路由：获取原始 attlog 数据
@attlog.route('/attlog/origin', methods=['GET'])
def get_origin_attlog():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM snort3_attlog LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in rows]
    return jsonify(result)


# 获取攻击信息占比
@attlog.route('/attlog/overview', methods=['GET'])
def get_attlog_overview():
    # 建立连接，获取数据库操作对象
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # 执行SQL语句查询相关信息
    cursor.execute("SELECT class, COUNT(*) AS count FROM snort3_attlog GROUP BY class ORDER BY count DESC")
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    cursor.execute("SELECT count(*) as cnt FROM snort3_attlog")
    totals = cursor.fetchall()[0]['cnt']
    # 关闭连接
    conn.close()
    for row in data:
        percent = row['count'] / totals
        del row['count']
        row['percent'] = percent
    return jsonify(data)
