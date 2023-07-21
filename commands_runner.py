import subprocess


class CommandsRunner:
    def __init__(self, command):
        self.command = command

    def runCmd(self):
        return subprocess.run(self.command, check=True, capture_output=True)
