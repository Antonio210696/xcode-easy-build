import yaml
import re
import argparse
from commands_runner import CommandsRunner


class BuildConfiguration:
    def __init__(self, actionConfiguration):
        self.scheme = actionConfiguration["scheme"]
        self.destination = actionConfiguration["destination"]
        self.workspace = actionConfiguration["workspace"]
        self.configuration = actionConfiguration["configuration"]


def readActionConfiguration(file, configurationName):
    yamlFile = open(file, "r")
    actionTree = yaml.safe_load(yamlFile)[configurationName]

    if actionTree["build"] is not None:
        buildAction = actionTree["build"]
        return BuildConfiguration(buildAction)


def runXcodeBuild(configuration):
    cmd = CommandsRunner(
        constructCommandFromConfiguration(configuration) + [
            "-showBuildSettings",
            "build"
        ]
    ).runCmd()

    return cmd


def getRelevantBuildOptions(buildOutput):
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


def constructCommandFromConfiguration(configuration):
    return [
        "xcodebuild",
        "-scheme",
        configuration.scheme,
        "-workspace",
        configuration.workspace,
        "-configuration",
        configuration.configuration,
        "-destination",
        configuration.destination,
        "-sdk",
        "iphonesimulator16.2"
    ]


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--input-file",
            type=str,
            help="""
            Input YAML file name.
            By default, the script looks for \"buildConfiguration.yml\"
            """)
    parser.add_argument(
            "confName",
            type=str,
            help="""
            Mandatory: configuration name to look inside the
            yml configuration file
            """)
    args = parser.parse_args()

    return args


def installAppOnBootedDevice(appPath):
    cmd = CommandsRunner(("xcrun simctl install booted " + appPath).split())
    cmd.runCmd()


def runAppOnBootedDevice(identifier):
    cmd = CommandsRunner(("xcrun simctl launch booted " + identifier).split())
    cmd.runCmd()


def main():
    args = parseArguments()

    filename = args.input_file
    if filename is None:
        filename = "buildConfiguration.yml"

    config = readActionConfiguration(filename, args.confName)
    print("Starting build")
    buildOutput = runXcodeBuild(config).stdout

    buildOptions = getRelevantBuildOptions(buildOutput)
    appPath = buildOptions[0] + "/" + buildOptions[1]
    productIdentifier = buildOptions[2]

    print("Install app on booted device")
    installAppOnBootedDevice(appPath)

    print("Launch app on booted device")
    runAppOnBootedDevice(productIdentifier)


if __name__ == "__main__":
    main()
