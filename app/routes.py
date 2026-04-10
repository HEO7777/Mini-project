"""Flask route definitions for the system monitor API."""

from app import app
from app.models import (
    get_cpu_usage,
    get_ram_usage,
    get_boot_time,
    get_top_processes,
    get_disk_usage,
    get_network_io,
    terminate_pid,
)
from flask import request, jsonify


@app.route('/api/cpu', methods=['GET'])
def cpu_usage():
    """Return current CPU usage.

    ---
    parameters: []
    responses:
      200:
        description: CPU usage returned successfully
        schema:
          type: object
          properties:
            cpu_percent:
              type: number
              format: float
    """
    return jsonify({"cpu_percent": get_cpu_usage()}), 200


@app.route('/api/ram', methods=['GET'])
def ram_usage():
    """Return current RAM usage summary.

    ---
    parameters: []
    responses:
      200:
        description: RAM usage returned successfully
        schema:
          type: object
          properties:
            percent:
              type: number
              format: float
            total_gb:
              type: number
              format: float
    """
    return jsonify(get_ram_usage()), 200


@app.route('/api/boot-time', methods=['GET'])
def boot_time():
    """Return system boot time.

    ---
    parameters: []
    responses:
      200:
        description: Boot time returned successfully
        schema:
          type: object
          properties:
            boot_time:
              type: string
    """
    return jsonify({"boot_time": get_boot_time().isoformat()}), 200


@app.route('/api/disk', methods=['GET'])
def disk_usage():
    """Return disk usage for a requested path.

    ---
    parameters:
      - name: path
        in: query
        type: string
        description: Filesystem path to inspect
        required: false
        default: /
    responses:
      200:
        description: Disk usage returned successfully
        schema:
          type: object
          properties:
            percent:
              type: number
              format: float
            total_gb:
              type: number
              format: float
    """
    path = request.args.get('path', '/')
    return jsonify(get_disk_usage(path)), 200


@app.route('/api/network', methods=['GET'])
def network_io():
    """Return network IO statistics.

    ---
    parameters: []
    responses:
      200:
        description: Network I/O returned successfully
        schema:
          type: object
          properties:
            bytes_sent_mb:
              type: number
              format: float
            bytes_recv_mb:
              type: number
              format: float
    """
    return jsonify(get_network_io()), 200


@app.route('/api/processes', methods=['GET'])
def top_processes():
    """Return the top running processes by memory usage.

    ---
    parameters:
      - name: limit
        in: query
        type: integer
        description: Number of processes to return
        required: false
        default: 20
    responses:
      200:
        description: Process list returned successfully
        schema:
          type: array
          items:
            type: object
            properties:
              pid:
                type: integer
              name:
                type: string
              memory_percent:
                type: number
                format: float
    """
    limit = request.args.get('limit', 20, type=int)
    processes = get_top_processes(limit)
    return jsonify(processes.to_dict(orient='records')), 200


@app.route('/api/process/kill', methods=['POST'])
def kill_process():
    """Terminate a process by PID.

    This endpoint accepts a JSON payload with a single integer property `pid`.

    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            pid:
              type: integer
              example: 1234
    consumes:
      - application/json
    responses:
      200:
        description: Process terminated successfully
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Bad request payload or invalid PID
        schema:
          type: object
          properties:
            error:
              type: string
      403:
        description: Permission denied while terminating the process
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Process not found
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()

    if not data or 'pid' not in data:
        return jsonify({"error": "No PID provided"}), 400

    pid = data.get('pid')

    if not isinstance(pid, int) or pid <= 0:
        return jsonify({"error": "Invalid PID format"}), 400

    try:
        terminate_pid(pid)
        return jsonify({"message": f"Process {pid} terminated successfully"}), 200
    except ValueError:
        return jsonify({"error": "Invalid PID format"}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except FileNotFoundError:
        return jsonify({"error": "Process not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
