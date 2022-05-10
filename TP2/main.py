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
  'include-after' : 'include after' 
}


expand_T1("templates_teste/template_md.txt",dictionary,"teste.txt")
#else: 
#  sys.exit("Invalid arguments")





