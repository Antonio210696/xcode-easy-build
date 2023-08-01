import yaml
import argparse
from build_command import BuildCommand
from run_command import RunCommand
from commands_runner import ICommandsRunner, CommandsRunner, VerboseCommandRunner, DryRunCommandRunner, CompositeCommandRunner


def readCommand(
        file: str,
        configurationName: str,
        commandsRunner: ICommandsRunner):
    yamlFile = open(file, "r")
    actionTree = yaml.safe_load(yamlFile)[configurationName]

    if "build" in actionTree.keys():
        buildAction = actionTree["build"]
        return BuildCommand(buildAction, commandsRunner)
    elif "run" in actionTree.keys():
        buildAction = actionTree["run"]
        return RunCommand(buildAction, commandsRunner)


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--input-file",
            type=str,
            help="""
            Input YAML file name.
            By default, the script looks for \"buildCommands.yml\"
            """)
    parser.add_argument(
            "commandName",
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
        filename = "buildCommands.yml"

    verboseRunner = VerboseCommandRunner()
    dryRunner = DryRunCommandRunner()
    commandsRunner = CompositeCommandRunner(
            verboseRunner=verboseRunner,
            dryRunner=dryRunner)

    command = readCommand(filename, args.commandName, commandsRunner)
    command.performAction()


if __name__ == "__main__":
    main()
