from commands_runner import ICommandsRunner
import abc


class ICommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def performAction(self):
        pass


class BuildCommand(ICommand):
    def __init__(
            self,
            commandConfiguration: dict,
            commandsRunner: ICommandsRunner):
        self.scheme = commandConfiguration["scheme"]
        self.destination = commandConfiguration["destination"]
        self.workspace = commandConfiguration["workspace"]
        self.configuration = commandConfiguration["configuration"]
        self.commandsRunner = commandsRunner

    def runXcodeBuild(self):
        self.commandsRunner.runCmd(
            self.constructCommandFromConfiguration() + [
                "-quiet",
                "build"
            ]
        )
        return self.commandsRunner.runCmd(
            self.constructCommandFromConfiguration() + [
                "-showBuildSettings"
            ]
        )

    def constructCommandFromConfiguration(self):
        return [
            "xcodebuild",
            "-scheme",
            self.scheme,
            "-workspace",
            self.workspace,
            "-configuration",
            self.configuration,
            "-destination",
            self.destination,
            "-sdk",
            "iphonesimulator16.2"
        ]

    def performAction(self):
        print("Starting build")
        self.runXcodeBuild()
