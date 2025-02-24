import psutil
import time

class SystemMonitor:
    @staticmethod
    def get_stats():
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "uptime": int(time.time() - psutil.boot_time())
        }