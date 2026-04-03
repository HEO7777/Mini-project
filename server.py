from flask import Flask, request, jsonify
from system_monitor import terminate_pid

app = Flask(__name__)

@app.route('/api/process/kill', methods=['POST'])
def kill_process():
    data = request.get_json()
    
    # 1. 클라이언트 데이터 검증 (Client-side verification logic simulation)
    if not data or 'pid' not in data:
        return jsonify({"error": "No PID provided"}), 400
    
    pid = data.get('pid')
    
    # 2. 데이터 타입 및 유효성 검증
    if not isinstance(pid, int) or pid <= 0:
        return jsonify({"error": "Invalid PID format"}), 400
    
    # 3. 보안 검증 (System Critical Process Protection)
    if pid == 1:
        return jsonify({"error": "Protected process"}), 403

    # 4. 프로세스 종료 로직 실행
    try:
        terminate_pid(pid)
        return jsonify({"message": f"Process {pid} terminated successfully"}), 200
    except ValueError:
        return jsonify({"error": "Invalid PID format"}), 400
    except PermissionError:
        return jsonify({"error": "Protected process"}), 403
    except psutil.NoSuchProcess:
        return jsonify({"error": "Process not found"}), 404
    except psutil.AccessDenied:
        return jsonify({"error": "Permission denied"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)