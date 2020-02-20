# -*- coding: utf-8 -*-
import os
import re
from uuid import uuid4
from py3o.template import Template
import sh
from lxml import objectify, etree
from erpbrasil.edoc.pdf import parser


DIRNAME = '/home/luisotavio/danfe'




#cte_namespace = lookup.get_namespace('http://www.portalfiscal.inf.br/cte')



class VoidElement():

    def __getattr__(self, item):
        if item == '__iter__':
            raise AttributeError
        return VoidElement()

    def __str__(self):
        return ''

    def __unicode__(self):
        return self.__str__()


def imprimir(string_xml=False, caminho_xml=False, output_dir=False):
    if caminho_xml:
        string_xml = open(caminho_xml,'rb').read()


    imprimir = ImprimirXml(string_xml, output_dir)
    imprimir.gera_pdf()




class ImprimirXml(object):

    def __init__(self, string_xml, output_dir):

        self.xml = string_xml
        self.output_dir = output_dir
        self.object_xml = objectify.fromstring(self.xml, parser=parser)

        self.imprime_canhoto = True
        self.logo = ''
        self.cabecalho = ''
        self.nome_sistema = ''

    def _gera_pdf(self, template):
        arq_template = self.output_dir + '/' + uuid4().hex
        open(arq_template, 'wb').write(template.read())
        template.close()

        arq_temp = uuid4().hex
        arq_odt = self.output_dir + '/' + arq_temp + '.odt'
        arq_pdf = self.output_dir + '/' + arq_temp + '.pdf'

        t = Template(arq_template, arq_odt)
        t.render({'danfe': self})

        lo = sh.libreoffice('--headless', '--invisible', '--convert-to',
                            'pdf', '--outdir', self.output_dir, arq_odt, _bg=True)
        lo.wait()

        self.conteudo_pdf = open(arq_pdf, 'rb').read()

        os.remove(arq_template)
        os.remove(arq_odt)
        os.remove(arq_pdf)

    def gera_pdf(self):
        template = open(os.path.join(self.output_dir, 'danfe.odt'), 'rb')
        self._gera_pdf(template)
        nome_arq = self.output_dir + \
            '/23200118386751000153550010000015991035334421' + '.pdf'
        open(nome_arq, 'wb').write(self.conteudo_pdf)
