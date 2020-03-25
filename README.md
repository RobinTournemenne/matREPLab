matREPLab
---------

This unique python file enhances the classic matlab command window in a terminal application. you just have to launch ```matREPLab.py``` instead of ```matlab -nodesktop```

This is espescially usefull when you want to code in editors different from the matlab native IDE (VS code, Sublime, Atom, emacs...) using the integrated terminals provided by those more advanced editors.

Quick start
-----------

make this file Callable using, for example: 

```shell
chmod 777 matREPLab.py; 
```

add an alias or add to yout ```PATH``` the matlab binary in your ~/.bashrc or ~/.bash_profile:

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
  - pexpect
  - prompt_toolkit

Features
--------
- color syntaxing
- go to errors (line and col) in files (VS code only for the moment)
- Auto completion (use the created file ```~/.matREPLab_completion_result```)
- history (use the created file ```~/.matREPLab_history```)
- multiline handling (a little bit cleaner than matlab -nodesktop)

Current validated environments and other equivalent contributions:
-----------------------------------------------------------------

Only tested on Mac OS X Mojave for the moment.
Should work just fine for any Unix OS.

To my knowledge only Calysto and imatlab (stange user name) implemented a jupyter kernel to improve matlab REPL in terminals:
- https://github.com/imatlab/imatlab
- https://github.com/Calysto/matlab_kernel

If matREPLab works on your environment, you don't need to install ```MATLAB engine for Python R2016b+``` contrary to these two other contributions, and you don't lose the debugging capabilities (dbstop is still working). 

Usefull not well known Matlab function:
---------------------------------------

To see variables in workspace:
```
>> workspace
```

To place breakspoints:
```
>> dbstop in myFile.m at line
```

Limitations:
------------

Output is printed when expression evaluation is finished (when the user get back the control). For long commands you can consult the created file ```~/..matREPLab_live_log``` which is written in real time (and also contains the autocompletion calls)

Planned Enhancements:
---------------------

- a settings management to chose themes and options
- check functionning on Linux and Windows system (via VS code)
- correct path completion
- common history with Matlab + plus special command for history monitoring
- real-time outputs
- integration in VS Code for breakpoints handling (and maybe more advanced stuff debugging navigation and )