from flask import Flask
from flask_socketio import SocketIO
from rcon import RCONClient
from system_monitor import SystemMonitor
from log_parser import LogParser

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/players')
def players():
    parser = LogParser("/home/corn/fabric_1.21/logs/latest.log")
    return {"players": parser.get_current_players()}

@app.route('/system_stats')
def system_stats():
    return SystemMonitor.get_stats()

@app.route('/test_rcon')
def test_rcon():
    rcon = RCONClient()
    try:
        return rcon.send_command("list")
    except Exception as e:
        return f"RCON Error: {str(e)}", 500
    
@app.route('/')
def hello():
    return "Minecraft Monitor Backend Running!"




from threading import Lock
thread = None
thread_lock = Lock()

def background_thread():
    while True:
        stats = SystemMonitor.get_stats()
        players = LogParser("/path/to/server.log").get_current_players()
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