import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'snort_logs.db')
# 绝对路径
# /var/log/snort/log
# /var/log/snort/detect
LOG_FILES = {
    'snort3_netlog': 'D:\\桌面\\学习文件\\大四上\\网络工程综合实践课设\\snort_log_project\\log\\alert_json.txt',
    'snort3_attlog': 'D:\\桌面\\学习文件\\大四上\\网络工程综合实践课设\\snort_log_project\\detect\\alert_json.txt'
}
