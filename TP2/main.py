import sys, re
from expand_T1 import *
from utilities import *
import yaml

error = False
#default dict
dictionary = {
  'lang' : 'en',
  'dir' : 'exemplo/exemplo',
  'author-meta' : ['autor-1','autor-2'],
  'author' : 'myself',
  'date-meta' : 'today',
  'keywords' : 'html_template',
  'sep' : ',',
  'title-prefix' : 'exemplo',
  'pagetitle' : 'pagina fixe',
  'quotes' : 'quote',
  'highlighting-css' : 'h-css',
  'css' : 'css',
  'math' : '1+1',
  'header-includes' : ['header 1','header 2'],
  'include-before' : ['include 1'],
  'title' : 'template',
  'idprefix' : 'prefixo',
  'subtitle' : 'subtitulo',
  'date' : 'today-date',
  'toc' : 'TOC',
  'body' : 'corpo do html',
  'include-after' : 'include after', 
  'teste' : {
    'fixe' : [1,3,5,6],
    'cool' : 'nice',
    'porreiro' : [
      {
      'another_one' : 'cool1'
    },
    {
      'another_one' : 'cool2'
    }
    ]
  }
}

re_name_file = r'^((.+)\\)?(?P<fn>(\w+(\.+)))(?P<ext>[yY][aA][mM][lL])$'
yamlC_match = re.compile(re_name_file)

if len(sys.argv) == 4:
  template_file = sys.argv[1]
  dictionary_file = sys.argv[2]
  output = sys.argv[3]

  
  if os.path.isfile(dictionary_file):
    if yamlC_match.match(dictionary_file):
      yaml_file = open(dictionary_file, 'r', encoding='utf8',errors="surrogateescape")
      yaml_to_dict = yaml.safe_load(yaml_file)
      yaml_file.close()
    else:
      dict_string = file_to_dict(dictionary_file)
      if dict_string:
        dictionary = dict_string
      else:
        print("Could not process dictionary file")
        error = True
  else:
    dict_string = ast.literal_eval(dictionary_file)
    if dict_string:
      dictionary = dict_string
    else:
      print("Invalid dictionary")
      error = True

  if not error:
    expand_T1(template_file,dictionary_file,output)


elif len(sys.argv) > 1 and len(sys.argv) < 4:
  template_file = sys.argv[1]
  output = sys.stdout

  #verificacao dos argumentos
  # segundo argumento pode ser um ficheiro de dicionario, um dicionario ou ficheiro de output
  if len(sys.argv) == 3:
    file = sys.argv[2]
    if os.path.isfile(file):
      if yamlC_match.match(file):
        yaml_file = open(file, 'r', encoding='utf8',errors="surrogateescape")
        dictionary = yaml.safe_load(yaml_file)
        yaml_file.close()
      else:
        dict_string = file_to_dict(file)
        if dict_string:
          dictionary = dict_string
        else:
          output = file
    else:
      dict_string = None
      try:
        dict_string = ast.literal_eval(file)
      except Exception:
        pass
      if dict_string:
        dictionary = dict_string
      else:
        print("Invalid dictionary")
        error = True

  if not error:
    expand_T1(template_file,dictionary,output)


else: 
  sys.exit("Invalid arguments")










