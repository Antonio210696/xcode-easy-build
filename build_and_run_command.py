import re
from commands_runner import ICommandsRunner
from build_command import BuildCommand


class BuildAndRunCommand(BuildCommand):
    def __init__(
            self,
            commandConfiguration,
            commandsRunner: ICommandsRunner):
        self.scheme = commandConfiguration["scheme"]
        self.destination = commandConfiguration["destination"]
        self.workspace = commandConfiguration["workspace"]
        self.configuration = commandConfiguration["configuration"]
        self.commandsRunner = commandsRunner

    def performAction(self):
        print("Starting build")
        buildOutput = self.runXcodeBuild().stdout

        buildOptions = self.getRelevantBuildOptions(buildOutput)
        appPath = buildOptions[0] + "/" + buildOptions[1]
        productIdentifier = buildOptions[2]

        print("Install app on booted device")
        self.installAppOnBootedDevice(appPath)

        print("Launch app on booted device")
        self.runAppOnBootedDevice(productIdentifier)

    def getRelevantBuildOptions(self, buildOutput):
        output = buildOutput.decode("utf-8").strip()

        targetBuildDir = re.search(
                r"TARGET_BUILD_DIR = (.*)",
                output,
                re.MULTILINE).group(1)
        executableFolderPath = re.search(
                r"EXECUTABLE_FOLDER_PATH = (.*)",
                output,
                re.MULTILINE).group(1)
        productBundleIdentifier = re.search(
                r"PRODUCT_BUNDLE_IDENTIFIER = (.*)",
                output,
                re.MULTILINE).group(1)
        return (targetBuildDir, executableFolderPath, productBundleIdentifier)

    def installAppOnBootedDevice(self, appPath):
        self.commandsRunner.runCmd(
                ("xcrun simctl install booted " + appPath).split())

    def runAppOnBootedDevice(self, identifier):
        self.commandsRunner.runCmd(
                ("xcrun simctl launch booted " + identifier).split())
