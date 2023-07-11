# Xcode Easy Build

The idea of this tool is simple: don't ever remember `xcodebuild` commands with all the input parameters such as **schemes, targets, simulators, projects and workspaces** hard names. 
This tool uses **YAML** configuration files that store all this information for you, and you can run several commands by creating other configurations.

## Usage

To run this tool, just run the script 

``` bash
xcode-easy-build.py <configuration-name>
```

where the `configuration-name` is the name of the configuration that you have prepared before, that will run a command with the specified arguments. The script by default
searches for a YAML file called `buildConfiguration.yml`. The user can specify a different file name, as explained below.

### Optional arguments

There is a list of optional arguments that can be specified when running the command.

* `--input-file`: specify the name for the configuration YAML file to look in the current directory.
