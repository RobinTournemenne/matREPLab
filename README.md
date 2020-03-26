matREPLab
---------

This unique python file enhances the classic matlab command window in a terminal application. you just have to launch ```matREPLab.py``` instead of ```matlab -nodesktop```

This is very usefull when you want to code in editors different from the matlab native IDE (VS code, Sublime, Atom, emacs...) using the integrated terminals provided by those more advanced editors.

Quick start
-----------

make this file callable using, for example: 

```shell
chmod 777 matREPLab.py
```

add an alias or add to your ```PATH``` the matlab binary in your ~/.bashrc or ~/.bash_profile (example for mac OS X):

```
PATH="/Applications/MATLAB_R2018b.app/bin:$PATH"
```
or

```
alias matlab="/Applications/MATLAB_R2018b.app/bin/matlab"
```

and execute it!

```shell
matREPLab.py
```

Requirements
------------
- Matlab
- python 3.6+
- python packages (installed via ```pip3 install package_name```):
  - pygments
  - pexpect (often already installed)
  - prompt_toolkit
  - pathlib (often already installed)

Features
--------
- color syntaxing
- go to errors (line and col) in files (VS code only for the moment)
- Auto completion (use the file ```~/.matREPLab_completion_result```)
- history (use the file ```~/.matREPLab_history```)
- multi-line handling (a little bit cleaner than matlab -nodesktop)

Current validated environments and other equivalent contributions:
-----------------------------------------------------------------

Should work on any Unix system (tested on Mac OS X and Ubuntu).

Working at least for Matlab 2016 to 2019. Does not work on Matlab 2020 because they removed access to the completion function. I may add a more basic solution to get completion results in this case, but it is not a priority.

To my knowledge only Calysto and imatlab (stange user name) implemented a jupyter kernel to improve matlab REPL in terminals:
- https://github.com/imatlab/imatlab
- https://github.com/Calysto/matlab_kernel

If matREPLab works on your environment, you don't need to install ```MATLAB engine for Python R2016b+``` contrary to these two other contributions, and you don't lose the debugging capabilities (dbstop is still working). 

Usefull not well known Matlab functions:
---------------------------------------

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

Limitations:
------------

Output is printed when expression evaluation is finished (when the user get back the control). For long commands you can consult the created file ```~/.matREPLab_live_log``` which is written in real time (and also contains the autocompletion calls)

Planned Enhancements:
---------------------

- a settings management to chose themes and options
- check functionning on Linux and Windows system (via VS code)
- common history with Matlab 
- special command for history monitoring
- real-time outputs
- integration in VS Code for breakpoints handling (and maybe more advanced stuff like debugging navigation and workspace visualization)

Aknowledgment:
---------------

This work has been possible thanks to the awesome [pexpect](https://github.com/pexpect/pexpect) project, [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) project and [pygments](https://github.com/pygments/pygments) project.