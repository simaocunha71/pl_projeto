import yaml
 
# sample json structure send by user.
yamlDict = {
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

 
# translate dictionary into yaml format.
print("DICIONARIO PARA YAML")
y = yaml.dump(yamlDict)
print(y)
print("-----------------")
print("YAML PARA DICIONARIO")
file = open("dictionaries/test2.yaml", "r")
yaml_dict = yaml.safe_load(file)
file.close()
print(yaml_dict)
