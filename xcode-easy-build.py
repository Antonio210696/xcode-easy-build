import yaml
import re
import subprocess
import argparse


class Configuration:
    def __init__(self, scheme, destination, workspace):
        self.scheme = scheme
        self.destination = destination
        self.workspace = workspace


def readConfiguration(file, configurationName):
    yamlFile = open(file, "r")
    object = yaml.safe_load(yamlFile)[configurationName]

    return Configuration(
            object["scheme"],
            object["destination"],
            object["workspace"])


def runXcodeBuild(configuration):
    subprocess.run(
        constructCommandFromConfiguration(configuration) + [
            "build"
        ]
    )


def getExecutablePath(configuration):
    ps = subprocess.run(
        constructCommandFromConfiguration(configuration) + [
            "-showBuildSettings"
        ],
        check=True,
        capture_output=True
    )

    output = ps.stdout.decode("utf-8").strip()
    targetBuildDir = re.search(
            r"TARGET_BUILD_DIR = (.*)",
            output,
            re.MULTILINE).group(1)
    executableFolderPath = re.search(
            r"EXECUTABLE_FOLDER_PATH = (.*)",
            output,
            re.MULTILINE).group(1)
    return targetBuildDir + "/" + executableFolderPath


def constructCommandFromConfiguration(configuration):
    return [
        "xcodebuild",
        "-scheme",
        configuration.scheme,
        "-workspace",
        configuration.workspace,
        "-destination",
        configuration.destination,
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


def main():
    args = parseArguments()

    filename = args.input_file
    if filename is None:
        filename = "buildConfiguration.yml"

    config = readConfiguration(filename, args.confName)
    print(getExecutablePath(config))
    #runXcodeBuild(config)


if __name__ == "__main__":
    main()
