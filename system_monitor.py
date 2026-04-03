import psutil
import pandas as pd
from datetime import datetime


def get_cpu_usage(interval=0.5):
    return psutil.cpu_percent(interval=interval)


def get_ram_usage():
    ram = psutil.virtual_memory()
    return {
        "percent": ram.percent,
        "total_gb": ram.total / (1024**3),
    }


def get_boot_time():
    return datetime.fromtimestamp(psutil.boot_time())


def get_top_processes(limit=20):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    df = pd.DataFrame(processes)
    df = df.sort_values(by='memory_percent', ascending=False).head(limit)
    df['memory_percent'] = df['memory_percent'].round(2)
    return df


def get_disk_usage(path='/'):
    disk = psutil.disk_usage(path)
    return {
        "percent": disk.percent,
        "total_gb": disk.total / (1024**3),
    }


def get_network_io():
    net = psutil.net_io_counters()
    return {
        "bytes_sent_mb": net.bytes_sent / (1024**2),
        "bytes_recv_mb": net.bytes_recv / (1024**2),
    }


def has_valid_pid(pid):
    return isinstance(pid, int) and pid > 1


def terminate_pid(pid):
    if pid == 1:
        raise PermissionError("Protected process")

    if not has_valid_pid(pid):
        raise ValueError("Invalid PID format")

    try:
        process = psutil.Process(pid)
        process.terminate()
        return True
    except psutil.NoSuchProcess:
        raise FileNotFoundError("Process not found")
    except psutil.AccessDenied:
        raise PermissionError("Permission denied")
