from commands_runner import CommandsRunner
import abc


class IConfiguration(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(
            self,
            actionConfiguration: dict,
            commandsRunner: CommandsRunner):
        pass


class BuildConfiguration(IConfiguration):
    def __init__(
            self,
            actionConfiguration: dict,
            commandsRunner: CommandsRunner):
        self.scheme = actionConfiguration["scheme"]
        self.destination = actionConfiguration["destination"]
        self.workspace = actionConfiguration["workspace"]
        self.configuration = actionConfiguration["configuration"]
        self.commandsRunner = commandsRunner

    def runXcodeBuild(self):
        return CommandsRunner().runCmd(
            self.constructCommandFromConfiguration() + [
                "-showBuildSettings",
                "build"
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
