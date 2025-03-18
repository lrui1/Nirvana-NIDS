from flask import Blueprint, jsonify, request
import sqlite3
from config import DB_PATH

# 创建 Blueprint
netlog = Blueprint('netlog', __name__)


# 获取自定义网络日志
@netlog.route('/netlog', methods=['GET'])
def get_cus_netlog():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, seconds,b64_data,dst_ap,ip_id,ip_len,msg,proto,rule,sid,src_ap,timestamp FROM snort3_netlog ORDER BY id DESC LIMIT ? OFFSET ?",
        (limit, offset))
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    cursor.execute("SELECT count(*) as cnt FROM snort3_netlog")
    totals = cursor.fetchall()
    conn.close()
    response = {
        "total": totals[0]['cnt'],
        "data": data
    }
    return jsonify(response)


# 路由：清空 netlog 数据
@netlog.route('/netlog', methods=['DELETE'])
def clear_netlog():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM snort3_netlog")
    conn.commit()
    conn.close()

    return jsonify({"message": "snort3_netlog table cleared."})


# 路由：获取原始 netlog 数据
@netlog.route('/netlog/origin', methods=['GET'])
def get_origin_netlog():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM snort3_netlog LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in rows]
    return jsonify(result)


# 获取网络日志HTTP占比
@netlog.route('/netlog/overview', methods=['GET'])
def get_http_count():
    # 建立连接，获取数据库操作对象
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # 执行SQL语句查询相关信息
    cursor.execute("SELECT count(*) as cnt FROM snort3_netlog where b64_data is not null")
    httpCountTotals = cursor.fetchall()
    cursor.execute("SELECT count(*) as cnt FROM snort3_attlog where b64_data is not null")
    evilHttpTotals = cursor.fetchall()
    # 关闭连接
    conn.close()

    httpCountTotals = httpCountTotals[0]['cnt']
    evilHttpTotals = evilHttpTotals[0]['cnt']
    evilPercent = evilHttpTotals / httpCountTotals
    response = {
        "evilPercent": evilPercent,
        "other": 1-evilPercent
    }
    return jsonify(response)
