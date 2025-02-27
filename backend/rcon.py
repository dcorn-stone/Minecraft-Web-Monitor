import subprocess
import os

class RCONClient:
    def __init__(self):
        self.host = os.getenv('RCON_HOST', '127.0.0.1')
        self.port = int(os.getenv('RCON_PORT', '25575'))
        self.password = os.getenv('RCON_PASSWORD', '')

    def send_command(self, command):
        try:
            result = subprocess.run(
                ['mcrcon', '-H', self.host, '-P', str(self.port), '-p', self.password, command],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"RCON Error: {e.stderr}"