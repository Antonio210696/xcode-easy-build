import re
from commands_runner import CommandsRunner
from build_configuration import BuildConfiguration


class BuildAndRunConfiguration(BuildConfiguration):
    def __init__(self, actionConfiguration):
        self.scheme = actionConfiguration["scheme"]
        self.destination = actionConfiguration["destination"]
        self.workspace = actionConfiguration["workspace"]
        self.configuration = actionConfiguration["configuration"]

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
        cmd = CommandsRunner(
                ("xcrun simctl install booted " + appPath).split())
        cmd.runCmd()

    def runAppOnBootedDevice(self, identifier):
        cmd = CommandsRunner(
                ("xcrun simctl launch booted " + identifier).split())
        cmd.runCmd()
