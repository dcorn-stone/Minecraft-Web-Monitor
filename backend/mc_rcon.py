from rcon.source import Client
import os

class RCONClient:
    def __init__(self):
        self.host = os.getenv('RCON_HOST', '127.0.0.1')
        self.port = int(os.getenv('RCON_PORT', '25575'))
        self.password = os.getenv('RCON_PASSWORD', '')

    def send_command(self, command):
        try:
            with Client(self.host, self.port, passwd=self.password) as client:
                response = client.run(command)
            return response.strip()
        except Exception as e:
            return f"RCON Error: {str(e)}"