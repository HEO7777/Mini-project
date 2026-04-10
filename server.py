"""Flask API entrypoint wrapper for the app package."""

from app import app
from flask import request, jsonify
from app.models import terminate_pid

@app.route('/api/process/kill', methods=['POST'])
def kill_process():
    """Terminate a process by PID.

    This endpoint accepts a JSON payload with a single integer property `pid`.
    It validates the request body, then forwards the termination request to the
    service layer in `app.models`.

    ---
    post:
      summary: Terminate a process by PID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                pid:
                  type: integer
                  example: 1234
      responses:
        200:
          description: Process terminated successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        400:
          description: Bad request payload or invalid PID
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        403:
          description: Permission denied while terminating the process
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        404:
          description: Process not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        500:
          description: Internal server error
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
    """
    data = request.get_json()

    # 1. 클라이언트 데이터 검증 (Client-side verification logic simulation)
    if not data or 'pid' not in data:
        return jsonify({"error": "No PID provided"}), 400
    
    pid = data.get('pid')
    
    # 2. 데이터 타입 및 유효성 검증
    if not isinstance(pid, int) or pid <= 0:
        return jsonify({"error": "Invalid PID format"}), 400
    
    # 3. 보안 검증은 서비스 레이어(system_monitor.terminate_pid)에서 수행

    # 4. 프로세스 종료 로직 실행
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

if __name__ == '__main__':
    app.run(debug=True)