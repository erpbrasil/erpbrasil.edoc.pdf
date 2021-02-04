# -*- coding: utf-8 -*-
import os
import re
import tempfile

import sh
from lxml import objectify
from py3o.template import Template

from erpbrasil.edoc.pdf import parser

# cte_namespace = lookup.get_namespace('http://www.portalfiscal.inf.br/cte')


class VoidElement(object):

    def __getattr__(self, item):
        if item == '__iter__':
            raise AttributeError
        return VoidElement()

    def __str__(self):
        return ''

    def __unicode__(self):
        return self.__str__()

    def __len__(self):
        return 0


class ImprimirXml(object):

    TIPOS_DOCUMENTOS = {
        'nfe': 'danfe',
    }

    def __init__(self, string_xml):

        self.string_xml = string_xml
        self.output_dir = None
        self.object_xml = objectify.fromstring(self.string_xml, parser=parser)
        self.tipo_impressao = None
        self.template = None
        self.pdf = None

        self.imprime_canhoto = True
        self.logo = ''
        self.cabecalho = ''
        self.nome_sistema = ''

    def _identifica_tipo_impressao(self):
        '''
        Identifica o tipo de documento de acordo com o final da url do
        parametro 'xmlns', da tag 'nfe'

        :return: str: tipo do documento
        '''

        url = self.object_xml.nsmap[None]
        documento = re.search(r'http://www.portalfiscal.inf.br/(.*)', url)
        if not documento:
            raise Exception('Não foi possível indentificar o tipo do '
                            'documento pelo XML')
        tipo = documento.group(1)

        tipo = self.TIPOS_DOCUMENTOS[tipo.lower()]

        return tipo

    def _renderiza_documento(self):
        '''
        Renderiza o documento e salva o pdf do tipo de documento especificado
        de acordo com o template correspondente

        :return:
        '''
        script_dir = os.path.dirname(__file__)
        template_path = os.path.join(script_dir, self.tipo_impressao + '.odt')
        template = open(template_path, 'rb')
        arq_template = tempfile.NamedTemporaryFile()
        arq_template.write(template.read())
        arq_template.seek(os.SEEK_SET)
        template.close()

        arq_odt = tempfile.NamedTemporaryFile(suffix=".odt")

        t = Template(arq_template.name, arq_odt.name)
        t.render({'danfe': self})

        lo = sh.libreoffice('--headless', '--invisible', '--convert-to',
                            'pdf', '--outdir', tempfile.gettempdir(),
                            arq_odt.name, _bg=True)
        lo.wait()

        arq_pdf = arq_odt.name[:-3] + 'pdf'
        self.pdf = open(arq_pdf, 'rb').read()

        arq_template.close()
        arq_odt.close()

    def _salva_pdf(self, output_dir):

        '''

        :param output_dir: (str): Caminho onde o arquivo pdf deve ser salvo no
        disco
        :return: (str): Caminho do PDF salvo no disco
        '''

        # Caso seja especificado o nome do arquivo a ser salvo no caminho de
        # parâmetro
        filename = os.path.basename(output_dir)[:-4]
        if filename:
            output_dir = output_dir.replace('.xml', '.pdf')
            open(output_dir, 'wb').write(self.pdf)
            return output_dir
        else:
            open(os.path.join(output_dir, 'danfe.pdf'), 'wb').write(self.pdf)
            return os.path.join(output_dir, 'danfe.pdf')

    @classmethod
    def imprimir(self, string_xml=False, caminho_xml=False, output_dir=False,
                 tipo_impressao=False):
        '''
        Método base para a impressão de documentos

        :param string_xml: (str): String do XML do documento
        :param caminho_xml: (str): Caminho para o arquivo XML do documento
        :param output_dir: (str): Caminho para salvar o documento PDF no disco
        :param tipo_impressao: (str): Tipo de impressão
        :return: (str): Conteúdo do arquivo PDF
        '''

        if caminho_xml:
            string_xml = open(caminho_xml, 'rb').read()

        obj = ImprimirXml(string_xml)

        # Identifica o tipo de documento a ser impresso
        if tipo_impressao:
            obj.tipo_impressao = tipo_impressao
        else:
            obj.tipo_impressao = obj._identifica_tipo_impressao()

        obj._renderiza_documento()

        # Salva PDF no disco
        if output_dir:
            return obj._salva_pdf(output_dir)

        return obj.pdf
