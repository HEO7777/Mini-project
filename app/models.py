"""System monitoring helpers for CPU, RAM, disk, network, and process control."""

import psutil
import pandas as pd
from datetime import datetime


def get_cpu_usage(interval=0.5):
    """Return the current CPU utilization percentage.

    Args:
        interval (float): Sampling interval in seconds for CPU measurement.

    Returns:
        float: CPU usage percentage.
    """
    return psutil.cpu_percent(interval=interval)


def get_ram_usage():
    """Return RAM usage details.

    Returns:
        dict: RAM usage summary with percent and total memory in gigabytes.
    """
    ram = psutil.virtual_memory()
    return {
        "percent": ram.percent,
        "total_gb": ram.total / (1024**3),
    }


def get_boot_time():
    """Return the system boot time as a datetime object.

    Returns:
        datetime: The time at which the system was last booted.
    """
    return datetime.fromtimestamp(psutil.boot_time())


def get_top_processes(limit=20):
    """Return the top running processes sorted by memory usage.

    Args:
        limit (int): Number of processes to return.

    Returns:
        pandas.DataFrame: Process list with pid, name, and memory_percent.
    """
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
    """Return disk usage metrics for a given filesystem path.

    Args:
        path (str): Filesystem path to inspect.

    Returns:
        dict: Disk usage summary with percent used and total size in gigabytes.
    """
    disk = psutil.disk_usage(path)
    return {
        "percent": disk.percent,
        "total_gb": disk.total / (1024**3),
    }


def get_network_io():
    """Return network input/output statistics since boot.

    Returns:
        dict: Network IO summary with bytes sent and received in megabytes.
    """
    net = psutil.net_io_counters()
    return {
        "bytes_sent_mb": net.bytes_sent / (1024**2),
        "bytes_recv_mb": net.bytes_recv / (1024**2),
    }


def has_valid_pid(pid):
    """Validate whether a PID is safe to attempt termination.

    Args:
        pid (int): Process identifier to validate.

    Returns:
        bool: True if pid is a valid integer greater than 1.
    """
    return isinstance(pid, int) and pid > 1


def terminate_pid(pid):
    """Attempt to terminate a process by PID.

    Args:
        pid (int): Process identifier to terminate.

    Raises:
        PermissionError: If the PID is protected or access is denied.
        ValueError: If pid is invalid.
        FileNotFoundError: If the process does not exist.

    Returns:
        bool: True if the termination request was issued.
    """
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
