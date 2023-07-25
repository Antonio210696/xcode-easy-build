import subprocess


class CommandsRunner:
    def runCmd(self, command: list) -> subprocess.CompletedProcess:
        return subprocess.run(command, check=True, capture_output=True)
