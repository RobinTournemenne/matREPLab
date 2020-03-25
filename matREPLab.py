#!/usr/local/bin/python3
from __future__ import unicode_literals

import time

from pathlib import Path
home = str(Path.home())

import json

import pygments
from pygments.lexers.matlab import MatlabLexer
from pygments.styles import get_style_by_name
from pygments.token import Token

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import PygmentsTokens

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.completion import Completer, Completion, FuzzyCompleter

import pexpect

def cleaning(text2Clean):
  text_cleaned = text2Clean.replace('{\x08', '\r\n')
  text_cleaned = text_cleaned.replace('}\x08', '')
  text_cleaned = text_cleaned.replace('[\x08', '')
  text_cleaned = text_cleaned.replace('\x1b[?1h\x1b=', '')
  text_cleaned = text_cleaned.replace('\x1b[?1h\x1b=\x1b[?1h\x1b=', '')
  return text_cleaned.replace(']\x08', '')

def outputDrawer(output_elements_list):
  for output_elements in output_elements_list:
    if len(output_elements) == 1:
      continue
    if output_elements[0].find('error') != -1: # if we called the function error
      print_formatted_text(HTML('<ansired>' + output_elements[1]  +'</ansired>'))
    elif output_elements[1].find('Error') != -1: # error in the executed function/script
      # vscode formatting
      parsedLineAndCol = output_elements[2].split(' ')
      output_elements[1]= output_elements[1] + ':' + parsedLineAndCol[1] + ':' + parsedLineAndCol[3] # for precise vscode navigation
  
      # terminal escape codes (works in zsh)
      # parsedName = outputElements[1].split(' ')
      # outputElements[1] = parsedName[0] + ' ' + parsedName[1] + "-e ''\e]8;;" + parsedName[2] + '\a' + parsedName[2] + '\e]8;;\a'
      error2Format = '\r\n'.join(output_elements[1:])
      print_formatted_text(HTML('<ansired>' + error2Format +'</ansired>'))
  
    elif output_elements[1].find('Warning') != -1:
      print_formatted_text(HTML('<ansiyellow>' + output_elements[1] +'</ansiyellow>'))
    elif output_elements[1].find('Undefined') != -1:
      print_formatted_text(HTML('<ansired>' + output_elements[1] +'</ansired>'))
    elif len(output_elements) > 3:
      tokens_input = list(pygments.lex(output_elements[1], lexer=MatlabLexer()))
      if output_elements[3].find('Error') != -1:
        print_formatted_text(PygmentsTokens(tokens_input[:-1]), style=style); print_formatted_text(HTML('<ansired>' + '\r\n'.join(output_elements[2:]) +'</ansired>'))
      elif output_elements[3].find('Warning') != -1: # I don't know if this occurs sometimes...
        print_formatted_text(PygmentsTokens(tokens_input[:-1]), style=style); print_formatted_text(HTML('<ansiyellow>' + '\r\n'.join(output_elements[2:]) +'</ansiyellow>'))
      else: # classic output (if long print)
        print_formatted_text('\r\n'.join(output_elements[1:]))
    else: #classic output (if short print)
      print_formatted_text('\r\n'.join(output_elements[1:]))

# styles = ['default','emacs','friendly','colorful','autumn','murphy','manni','monokai','perldoc','pastie','borland','trac','native','fruity','bw','vim','vs','tango','rrt','xcode','igor','paraiso-light','paraiso-dark','lovelace','algol','algol_nu','arduino','rainbow_dash','abap','solarized-dark','solarized-light','sas','stata','stata-light','stata-dark','inkpot']
style_name = 'solarized-dark'
style = style_from_pygments_cls(get_style_by_name(style_name))

session = PromptSession(history=FileHistory('/Users/robintournemenne/.matREPLab_history'))
child = pexpect.spawn('/bin/bash -c "matlab -nodesktop | tee ~/.matREPLab_live_log"')

class MatlabCompleter(Completer):
    def get_completions(self, document, complete_event):
      word = document.get_word_before_cursor()
      expression = document.current_line
      expression_matlabed = expression.replace('\'', '\'\'')

      child.sendline('a = com.mathworks.jmi.MatlabMCR().mtGetCompletions(\'' + expression_matlabed + '\',' + str(len(expression)) + '); fid = fopen(\'~/.matREPLab_completion_result\',\'w\'); fprintf(fid, \'%s\',a); fclose(fid);')
      child.expect('>> $')
      with open(home + '/.matREPLab_completion_result') as json_file:
        matlab_completion_output = json.load(json_file)
      if 'cannotComplete' in matlab_completion_output:
        pass
      else:
        if 'finalCompletions' in matlab_completion_output:
          completion_propositions = matlab_completion_output['finalCompletions']
        else:
          completion_propositions = []
        for proposition in completion_propositions:
          if expression.find('(') != -1: # completion inside a function signature
            if (word == '(') | (word == '(\'') | (word == ',') | (word == '\',') | (word == '\',\''):
              yield Completion(proposition['popupCompletion'], start_position=0, display=proposition['popupCompletion'])
            elif word == '\'':
              pass
            else:
              yield Completion(proposition['popupCompletion'], start_position=-len(word), display=proposition['popupCompletion'])
          else:
            yield Completion(proposition['popupCompletion'], start_position=-len(expression))


child.expect('>>')
rawIntro = cleaning(child.before.decode('utf-8'))
# the following lexing is not interesting since it is not matlab code to ptompt but it shows directly to the user that the extension works or not
tokens = list(pygments.lex(rawIntro, lexer=MatlabLexer()))
print_formatted_text(PygmentsTokens(tokens), style=style)

while(1):
  user_input = session.prompt('>> ', lexer=PygmentsLexer(MatlabLexer), style=style, include_default_pygments_style=False, completer=MatlabCompleter())
  child.sendline(user_input)
  if user_input == 'exit':
    break
  time.sleep(0.1)
  child.expect('>> $') # the dollar is used for multiline inputs if I record well

  raw_text = child.before.decode('utf-8')

  raw_text = cleaning(raw_text)
  output_elements2categorize = raw_text.split('\r\n')
  if user_input.find('\n') != -1:
    if user_input.find('\r') != -1:
      user_input_parsed = user_input.split('\r\n')
    else:
      user_input_parsed = user_input.split('\n')
    current_idx = 0
    output_elements_list = []
    for element in output_elements2categorize:
      if current_idx != len(user_input_parsed):
        if element.find(user_input_parsed[current_idx]) != -1:
          current_idx += 1
          output_elements_list.append(['simulating the first one Liner stdout'])
          if current_idx == 1:
            output_elements_list[current_idx - 1].append('')
        else:
          output_elements_list[current_idx - 1].append(element)
      else:
        output_elements_list[current_idx - 1].append(element)
  else: #single line entered by the user
    output_elements_list = [output_elements2categorize]
  outputDrawer(output_elements_list)

child.kill(1)