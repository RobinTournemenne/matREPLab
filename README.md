matREPLab
=========

This unique python file enhances the classic matlab command window in a terminal application. you just have to launch ```matreplab``` instead of ```matlab -nodesktop```. This can also be used for people using the ```-nojvm``` flag (see the settings section).

This is very usefull when you want to code in editors different from the matlab native IDE (VS code, Sublime, Atom, emacs...) using the integrated terminals provided by those more advanced editors.

Quick start
===========

for most people:

```shell
> pip3 install matreplab
```

for Mac OS X people, instead of pip you can use brew with the slight advantage of leaving your python site-package virgin of matreplab if it matters to you:

```shell
> brew tap RobinTournemenne/matreplab  
> brew install matreplab
```

Then you need to make the command ```matlab``` executable by creating an alias, or adding it to your path in your ~/.bashrc or ~/.bash_profile (example for mac OS X):

```
PATH="/Applications/MATLAB_R2018b.app/bin:$PATH"
```
or

```
alias matlab="/Applications/MATLAB_R2019a.app/bin/matlab"
```

and then simply:

```shell
> matreplab
```

Troubleshooting
===============

Basically, what pip (python package management system) does is creating a shebang in the script and place it in an executable folder in your PATH. 

If for some reason this ```pip install``` doesn't work, you just have to do that yourself, which is not a hustle: 

1. Clone this repository, or simply download the file ```matREPLab```

2. cd in the cloned folder and make this file executable using, for example:

```shell
> chmod +x matREPLab
```

3. install the 4 dependencies manually via ```pip3 install package_name``` (Cf. Requirements)

4. execute it!

```shell
> matREPLab
```

if it is still not working, maybe the shebang doesn't work and you will have to force the usage of ```python3```:

```shell
> python3 matREPLab
```

Requirements
============
- Matlab
- python 3.6+
- python packages (installed via ```pip3 install package_name```):
  - pygments
  - pexpect (often already installed)
  - prompt_toolkit
  - pathlib (often already installed)

Features
========
- color syntaxing
- Auto completion (use the file ```~/.matREPLab_completion_result```)
- go to errors (line and col) in files (VS code only for the moment)
- history (use the file ```~/.matREPLab_history```)
- multi-line handling (a little bit cleaner than matlab -nodesktop)

magic functions and settings
============================
Startup
-------
One can tune matREPLab at launch with the following flags:
- ```-matlab_flags``` (change the flags called by maltab, replacing for example -nodesktop by -nojvm)
- ```-theme```
- ```-disable_auto_suggest```
- ```-complete_while_typing```
- ```-disable_history_search```
- ```-settings_filename``` (not possible tu use relative path or ~)
- ```-history_filename``` (should be useless)
- ```-completion_filename``` (should be useless)
- ```-log_filename``` (should be useless)
- ```-disable_complete_in_threads``` (disable responsive completer, should be useless)

examples:
```shell
> matreplab -matlab_flags="-nojvm -nosplash"
```

```shell
> matreplab -theme="stata-dark" -disable_auto_suggest
```

```shell
> matreplab -settings_filename="/Users/me/Document/MATLAB/myAwesomeMatREPLabSettings.json"
```

Some functions has been added specifically to try options directly inside the REPL (they are called magic functions):

- ```%setSettings``` to change settings parameters writting directly a json array as a string. Here are the possible couples Name/Values:
  - ```matlab_flags```: string
  - ```theme```: string
  - ```history_search```: true/false
  - ```auto_suggest```: true/false
  - ```complete_while_typing```: true/false
  - ```complete_in_threads```: true/false
  - ```settings_filename```: string
  - ```history_filename```: string
  - ```completion_filename```: string
  - ```log_filename```: string

example: 
```shell
>> %setSettings {"theme":"stata-dark", "complete_while_typing":true, "auto_suggest":false}
```

- ```%saveSettings``` to record the settings in a file (~/.matREPLab_settings by default) which will be loaded at matREPLab startup
- ```%getAvailableThemes```which print a list of currently available themes in your pygments package.

Current validated environments and other equivalent contributions
=================================================================

Should work on any Unix system (tested on Mac OS X Mojave and Ubuntu 18.04).

Working at least for Matlab 2016 to 2019. Does not work on Matlab 2020 because they removed access to the auto-completion function. I may add a more basic solution to get completion results in this case, but it is not a priority.

To my knowledge only Calysto and imatlab (stange user name) implemented a jupyter kernel to improve matlab REPL in terminals:
- https://github.com/imatlab/imatlab
- https://github.com/Calysto/matlab_kernel

If matREPLab works on your environment, you don't need to install ```MATLAB engine for Python R2016b+``` contrary to these two other contributions, and you don't lose the debugging capabilities (dbstop is still working). 

Usefull not well known Matlab functions
=======================================

To see variables in workspace:
```
>> workspace
```

To place breakspoints:
```
>> dbstop in myFile.m at line
```

To consult pretty documentation:
```
>> doc num2str
```

To consult the actual Matlab history (not the one of matREPLab):
```
>> commandhistory
```

Limitations
===========

Output is printed when expression evaluation is finished (when the user get back the control). For long commands outputing some information, you can consult the created file ```~/.matREPLab_live_log``` which is written in real time (and also contains the autocompletion calls).

You cannot change the auto-suggest from false to true inside matREPLab.

Planned Enhancements
====================

- real-time outputs +making input possible
- keyboard interrupt, interrupts also matlab code
- validator for settings file! to avoid useless keys in json
- check functionning on Windows system (via VS code)
- common history with Matlab 
- special command for history monitoring
- shared matlab session magic function
- integration in VS Code for breakpoints handling (and maybe more advanced stuff like debugging navigation and workspace visualization)

Aknowledgment
=============

This work has been possible thanks to the awesome [pexpect](https://github.com/pexpect/pexpect) project, [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) project and [pygments](https://github.com/pygments/pygments) project.