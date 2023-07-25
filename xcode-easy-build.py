import yaml
import argparse
from build_configuration import BuildConfiguration
from build_and_run_configuration import BuildAndRunConfiguration


def readActionConfiguration(file, configurationName):
    yamlFile = open(file, "r")
    actionTree = yaml.safe_load(yamlFile)[configurationName]

    if "build" in actionTree.keys():
        buildAction = actionTree["build"]
        return BuildConfiguration(buildAction)
    elif "build_and_run" in actionTree.keys():
        buildAction = actionTree["build_and_run"]
        return BuildAndRunConfiguration(buildAction)


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
