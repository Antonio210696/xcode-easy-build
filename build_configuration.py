from commands_runner import CommandsRunner


class BuildConfiguration:
    def __init__(self, actionConfiguration):
        self.scheme = actionConfiguration["scheme"]
        self.destination = actionConfiguration["destination"]
        self.workspace = actionConfiguration["workspace"]
        self.configuration = actionConfiguration["configuration"]

    def runXcodeBuild(self):
        cmd = CommandsRunner(
            self.constructCommandFromConfiguration() + [
                "-showBuildSettings",
                "build"
            ]
        ).runCmd()

        return cmd

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
