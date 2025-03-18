from app import create_app
from app.monitor import start_monitoring
import threading

app = create_app()

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def run_monitor():
    observer = start_monitoring()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    # 创建两个线程分别运行 Flask 和文件监控
    flask_thread = threading.Thread(target=run_flask)
    monitor_thread = threading.Thread(target=run_monitor)

    flask_thread.start()
    monitor_thread.start()

    flask_thread.join()
    monitor_thread.join()
