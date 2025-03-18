import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.database import insert_data
from config import LOG_FILES


class LogFileHandler(FileSystemEventHandler):
    def __init__(self, table_name):
        self.table_name = table_name
        self.file_position = 0  # 跟踪文件读取位置

    def on_modified(self, event):
        # print(event.src_path)
        # print(os.path.abspath(event.src_path))
        # 使用规范化路径进行比较
        if os.path.abspath(event.src_path) == LOG_FILES[self.table_name]:
            try:
                with open(event.src_path, 'r', encoding='utf-8') as file:
                    # 跳转到上次读取的位置
                    file.seek(self.file_position)

                    # 读取新增内容
                    for line in file:
                        line = line.strip()
                        if line:  # 跳过空行
                            try:
                                data = json.loads(line)
                                insert_data(self.table_name, data)
                            except json.JSONDecodeError as e:
                                print(f"Invalid JSON in {event.src_path}: {e}")

                    # 更新当前位置
                    self.file_position = file.tell()
            except Exception as e:
                print(f"Error processing file {event.src_path}: {e}")


def start_monitoring():
    observer = Observer()
    for table_name, file_path in LOG_FILES.items():
        handler = LogFileHandler(table_name)
        observer.schedule(handler, path=os.path.dirname(file_path), recursive=False)

    observer.start()
    print("Monitoring started...")
    return observer


if __name__ == "__main__":
    # 初始化监控器
    observer = start_monitoring()

    try:
        while True:
            pass  # 保持主线程运行
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring stopped.")

    observer.join()
