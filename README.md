# Xcode Easy Build

The idea of this tool is simple: don't ever remember `xcodebuild` commands with
all the input parameters such as **schemes, targets, simulators, projects and
workspaces** hard names. This tool uses **YAML** configuration files that store
all this information for you, and you can run several commands by creating
other configurations.

## Lexical

In order to better grasp how this project is intended to work, let's give a
brief summary of the vocabulary used: 

- **Action**: it is the operation (or set of operations) that will be performed
	with the codebase. An action isn't intended to modify the content of the
	project, but just to perform operations with it (e.g. building, testing,
	running, etc...)
- **Configuration**: a configuration is the set of parameters with which an
	action runs. Each action requires a different set of parameters.
- **Command**: this is the combination of action and configuration that can be
	selected to be performed when running the script

## Usage

To run this tool, just run the script 

``` bash 
xcode-easy-build.py <command1> <command2> ... 
```

where `commandX` is the name of a command that you have prepared before in
the configuration file. It will run a command with the arguments specified in
the configuration file. An arbitrary number of commands can be specified: they
will all run **one after the other** The script by default searches for a YAML
file called `buildCommands.yml`. The user can specify a different file name, as
explained below.

### Optional arguments

There is a list of optional arguments that can be specified when running the
command.

- `--input-file`: specify the name for the configuration YAML file to look in
	the current directory.

### Example of `buildCommands.yml`

```yaml
buildApp:
  build:
    destination: "platform=iOS Simulator,name=iPhone 14"
    scheme: "AppScheme"
    workspace: "App.xcworkspace"
    configuration: "Debug"
```
