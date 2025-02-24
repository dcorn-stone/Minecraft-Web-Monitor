import re

class LogParser:
    JOIN_PATTERN = r"(\w+) joined the game"
    LEAVE_PATTERN = r"(\w+) left the game"

    def __init__(self, log_path):
        self.log_path = log_path

    def get_current_players(self):
        with open(self.log_path, 'r') as f:
            log_content = f.read()
            joins = re.findall(self.JOIN_PATTERN, log_content)
            leaves = re.findall(self.LEAVE_PATTERN, log_content)
            return list(set(joins) - set(leaves))