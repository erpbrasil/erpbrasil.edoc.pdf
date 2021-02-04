from os import path
from os import walk

from erpbrasil.edoc.pdf import base

PATH = 'xml'
OUTPUT = 'output'
TIPO = 'danfe'

for (dirpath, dirnames, filenames) in walk(PATH):
    for file in filenames:
        arquivo = path.join(PATH, file)
        output = path.join(OUTPUT, file)

        print('XML: ' + file)
        print(base.ImprimirXml.imprimir(caminho_xml=arquivo, output_dir=output))
