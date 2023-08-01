from build_based_command import BuildBasedCommand
from commands_runner import ICommandsRunner


class BuildCommand(BuildBasedCommand):
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

    def performAction(self):
        print("Starting build")
        self.runXcodeBuild()
