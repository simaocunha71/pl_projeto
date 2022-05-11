import sys, re
from expand_T1 import *
import yaml

template_file = sys.argv[1]
dictionary_file = sys.argv[2]
output = sys.argv[3]

yaml_file = open(dictionary_file, 'r', encoding='utf8',errors="surrogateescape")
re_name_file = r'^((.+)\\)?(?P<fn>(\w+(\.+)))(?P<ext>[yY][aA][mM][lL])$'
yamlC_match = re.compile(re_name_file)


if (yamlC_match.match(dictionary_file)):
  yaml_to_dict = yaml.safe_load(yaml_file)
  expand_T1(template_file,yaml_to_dict,output)
else:
  expand_T1(template_file,dictionary_file,output)

yaml_file.close()


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



#file = sys.stdout
#print(dic_contains("it.porreiro.another_one",dictionary,"teste.porreiro",2,1))
#dic_write_var("teste.fixe",dictionary,file,"teste.porreiro",2,0)
#file.close()


#else: 
#  sys.exit("Invalid arguments")










