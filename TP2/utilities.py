import re

def matches_to_tuples(matches):
  tuple_stack = []
  for match in matches:
      type = match.group(1)
      content = ""
      if match.group(3):
       content = remove_qotes(match.group(3))
      tuple = (type,content)
      tuple_stack.append(tuple)
  return tuple_stack

def remove_qotes(string):
  reg_exp = r'"(.+|\n+|\s+)"'
  compile = re.compile(reg_exp)
  match = compile.search(string)
  if match:
    return match.group(1)
  else:
    return string

def remove_dolars(string):
  reg_exp = r'\$(.+)\$'
  compile = re.compile(reg_exp)
  match = compile.search(string)
  if match:
    return match.group(1)
  else:
    return string