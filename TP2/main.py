import sys
from expand_T1 import *

#if(len(sys.argv) == 3):
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

expand_T1("templates_teste/template_html.txt",dictionary,"teste.txt")
#else: 
#  sys.exit("Invalid arguments")





