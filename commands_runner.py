import subprocess
import abc


class ICommandsRunner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def runCmd(self, command: list) -> subprocess.CompletedProcess:
        pass


class CommandsRunner(ICommandsRunner):
    def runCmd(self, command: list) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(command, check=True, capture_output=True)
        except subprocess.CalledProcessError as error:
            print(error.stdout.decode("utf-8"))
            print(error.stderr.decode("utf-8"))
            exit(error.returncode)


class VerboseCommandRunner(ICommandsRunner):
    def runCmd(self, command: list) -> subprocess.CompletedProcess:
        try:
            process = subprocess.run(command, check=True, capture_output=True)
            print(process.stdout.decode("utf-8"))
            return process
        except subprocess.CalledProcessError as error:
            print(error.stdout.decode("utf-8"))
            print(error.stderr.decode("utf-8"))
            exit(error.returncode)


class DryRunCommandRunner(ICommandsRunner):
    def runCmd(self, command: list) -> subprocess.CompletedProcess:
        print(' '.join(command))
        return None


class CompositeCommandRunner(ICommandsRunner):
    def __init__(
            self,
            defaultRunner=CommandsRunner(),
            verboseRunner: VerboseCommandRunner = None,
            dryRunner: DryRunCommandRunner = None):
        self.defaultRunner = defaultRunner
        self.verboseRunner = verboseRunner
        self.dryRunner = dryRunner

    def runCmd(self, command: list) -> subprocess.CompletedProcess:
        if self.dryRunner is not None:
            self.dryRunner.runCmd(command)

        if self.verboseRunner is not None:
            return self.verboseRunner.runCmd(command)
        else:
            return self.defaultRunner.runCmd(command)
