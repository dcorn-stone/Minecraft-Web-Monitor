from mcrcon import MCRcon
import os

class RCONClient:
    def __init__(self):
        self.host = os.getenv('RCON_HOST', '127.0.0.1')
        self.port = int(os.getenv('RCON_PORT', 25575))
        self.password = os.getenv('RCON_PASSWORD', '')

    def send_command(self, command):
        with MCRcon(self.host, self.password, self.port) as mcr:
            return mcr.command(command)