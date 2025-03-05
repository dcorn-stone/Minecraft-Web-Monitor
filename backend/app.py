from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from mc_rcon import RCONClient
from system_monitor import SystemMonitor
from log_parser import LogParser
from threading import Lock


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return 'Index Page'

@app.route('/api/players', methods=['GET'])
def players():
    parser = LogParser("/home/corn/fabric_1.21/logs/latest.log")
    return {"players": parser.get_current_players()}

@app.route('/api/system_stats', methods=['GET'])
def system_stats():
    return SystemMonitor.get_stats()

    


@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    command = data.get('command')
    if not command:
        return jsonify({"error": "Command is required"}), 400

    rcon = RCONClient()
    try:
        response = rcon.send_command(command)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


thread = None
thread_lock = Lock()

def background_thread():
    while True:
        stats = SystemMonitor.get_stats()
        players = LogParser("/home/corn/fabric_1.21/logs/latest.log").get_current_players()
        socketio.emit('update', {
            'stats': stats,
            'players': players
        })
        socketio.sleep(5)  # 5秒更新一次

@socketio.on('connect')
def handle_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)



if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)