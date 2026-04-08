import psuti #library tool fr checking system statscheck CPU %, Memory %, Disk %
import logging #library (tool for writing messages)logging.basicConfig(level=lo
from typing import Dict, List
from datetime import datetime
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class SystemHealthChecker:
    """Monitor system health metrics."""
    def __init__(self, cpu_threshold=80, memory_threshold=80, disk_threshold=80):
    """
    Initialize health checker with thresholds.

    Args:
        cpu_threshold: CPU usage percentage (default: 80%)
        memory_threshold: Memory usage percentage (default: 80%)
        disk_threshold: Disk usage percentage (default: 80%)
    """
    self.cpu_threshold = cpu_threshold
    self.memory_threshold = memory_threshold
    self.disk_threshold = disk_threshold
    logger.info("SystemHealthChecker initialized")

    def check_cpu(self) -> Dict:
    """Check CPU usage."""
    cpu_percent = psutil.cpu_percent(interval=1)
    status = "CRITICAL" if cpu_percent > self.cpu_threshold else "OK"

    logger.info(f"CPU Check: {cpu_percent}% - {status}")

    return {
        "metric": "CPU",
        "value": cpu_percent,
        "threshold": self.cpu_threshold,
        "status": status,
        "unit": "%",
        "timestamp": datetime.now().isoformat()
    }
    def check_memory(self) -> Dict:
    """Check memory usage."""
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    status = "CRITICAL" if memory_percent > self.memory_threshold else "OK"

    logger.info(f"Memory Check: {memory_percent}% - {status}")

    return {
        "metric": "MEMORY",
        "value": memory_percent,
        "threshold": self.memory_threshold,
        "status": status,
        "unit": "%",
        "timestamp": datetime.now().isoformat(),
        "total_gb": round(memory.total / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2)
    }
    def check_disk(self) -> Dict:
    """Check disk usage."""
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    status = "CRITICAL" if disk_percent > self.disk_threshold else "OK"

    logger.info(f"Disk Check: {disk_percent}% - {status}")

    return {
        "metric": "DISK",
        "value": disk_percent,
        "threshold": self.disk_threshold,
        "status": status,
        "unit": "%",
        "timestamp": datetime.now().isoformat(),
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2)
    }
    def check_all(self) -> List[Dict]:
    """Check all system metrics."""
    logger.info("Starting full system health check...")

    results = [
        self.check_cpu(),
        self.check_memory(),
        self.check_disk()
    ]

    critical_count = sum(1 for r in results if r["status"] == "CRITICAL")
    if critical_count > 0:
        logger.warning(f"⚠️ Found {critical_count} CRITICAL metrics!")
    else:
        logger.info("✅ All systems healthy!")

    return results



