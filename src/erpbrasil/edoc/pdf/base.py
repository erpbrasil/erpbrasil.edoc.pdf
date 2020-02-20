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







class DanfeXml(object):

    def __init__(self):
        self.xml = open(
            DIRNAME + '/exemplos_nfe/nProt_135190157727764_v4.00-procNFe.xml',
            'rb'
        ).read()

        self.object_xml = objectify.fromstring(self.xml, parser=parser)

        self.imprime_canhoto = True
        self.logo = ''
        self.cabecalho = ''
        self.nome_sistema = ''

    def _gera_pdf(self, template):
        arq_template = DIRNAME + '/' + uuid4().hex
        open(arq_template, 'wb').write(template.read())
        template.close()

        arq_temp = uuid4().hex
        arq_odt = DIRNAME + '/' + arq_temp + '.odt'
        arq_pdf = DIRNAME + '/' + arq_temp + '.pdf'

        t = Template(arq_template, arq_odt)
        t.render({'danfe': self})

        lo = sh.libreoffice('--headless', '--invisible', '--convert-to',
                            'pdf', '--outdir', DIRNAME, arq_odt, _bg=True)
        lo.wait()

        self.conteudo_pdf = open(arq_pdf, 'rb').read()

        os.remove(arq_template)
        os.remove(arq_odt)
        os.remove(arq_pdf)

    def gerar_danfe(self):
        template = open(os.path.join(DIRNAME, 'danfe.odt'), 'rb')
        self._gera_pdf(template)
        nome_arq = DIRNAME + \
            '/23200118386751000153550010000015991035334421' + '.pdf'
        open(nome_arq, 'wb').write(self.conteudo_pdf)
