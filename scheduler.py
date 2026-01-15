import schedule
import time
from typing import Callable
from config import Config


class TaskScheduler:
    def __init__(self, config: Config):
        self.config = config
        self.running = False
    
    def schedule_task(self, task_func: Callable, time_str: str = None):
        if time_str is None:
            time_str = self.config.get_schedule_time()
        
        schedule.every().day.at(time_str).do(task_func)
        print(f"定时任务已设置: 每天 {time_str} 执行")
    
    def run(self):
        self.running = True
        print("定时任务调度器已启动...")
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)
    
    def stop(self):
        self.running = False
        print("定时任务调度器已停止")
    
    def run_once(self, task_func: Callable):
        print("执行一次性任务...")
        task_func()
