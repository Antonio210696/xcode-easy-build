from commands_runner import ICommandsRunner
import abc


class IConfiguration(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def performAction(self):
        pass


class BuildConfiguration(IConfiguration):
    def __init__(
            self,
            actionConfiguration: dict,
            commandsRunner: ICommandsRunner):
        self.scheme = actionConfiguration["scheme"]
        self.destination = actionConfiguration["destination"]
        self.workspace = actionConfiguration["workspace"]
        self.configuration = actionConfiguration["configuration"]
        self.commandsRunner = commandsRunner

    def runXcodeBuild(self):
        self.commandsRunner.runCmd(
            self.constructCommandFromConfiguration() + [
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
