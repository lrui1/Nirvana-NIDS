from flask import Flask
from flask_cors import CORS
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    # 初始化数据库
    init_db()

    # 注册主路由
    # from app.main_routes import main
    # app.register_blueprint(main)

    # 注册 netlog 路由
    from app.netlog_routes import netlog
    app.register_blueprint(netlog)

    # 注册 attlog 路由
    from app.attlog_routes import attlog
    app.register_blueprint(attlog)

    # 全局开启跨域请求通行
    CORS(app)

    return app
