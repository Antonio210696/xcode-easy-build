from commands import ICommand


class BuildBasedCommand(ICommand):
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
