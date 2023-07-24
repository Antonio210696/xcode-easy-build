import yaml
import re
import argparse
from commands_runner import CommandsRunner
from build_configuration import BuildConfiguration


def readActionConfiguration(file, configurationName):
    yamlFile = open(file, "r")
    actionTree = yaml.safe_load(yamlFile)[configurationName]

    if actionTree["build"] is not None:
        buildAction = actionTree["build"]
        return BuildConfiguration(buildAction)


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

    config = readActionConfiguration(filename, args.confName)
    config.performAction()


if __name__ == "__main__":
    main()
