import re

from lxml import objectify

from erpbrasil.edoc.pdf import danfe_formata
from erpbrasil.edoc.pdf import lookup
from erpbrasil.edoc.pdf.base import VoidElement

nfe_namespace = lookup.get_namespace('http://www.portalfiscal.inf.br/nfe')

# Campos que podem não existir no XML da NF-e
NAO_OBRIGATORIO = [
    'veicTransp', 'placa', 'fone', 'transporta', 'vTotTrib', 'marca', 'nVol',
    'pesoL', 'vIPI', 'vol', 'IEST', 'CST', 'pIPI', 'RNTC', 'dhSaiEnt',
    'indPag', 'vBC', 'vICMS', 'pICMS', 'cobr', 'qVol', 'esp', 'pesoB', 'IE',
    'IPI', 'nFat', 'vDesc',
]

TAGS_ICMS = [
    'ICMS00',
    'ICMS10',
    'ICMS20',
    'ICMS30',
    'ICMS40',
    'ICMS50',
    'ICMS60',
    'ICMS70',
    'ICMS80',
    'ICMS90',
    'ICMSSN101',
    'ICMSSN102',
    'ICMSSN201',
    'ICMSSN202',
    'ICMSSN500',
    'ICMSSN900',
    'ICMSPart',
    'ICMSST'
]

TAGS_IPI = [
    'IPINT',
    'IPITrib',
]


@nfe_namespace(None)
class NFeElement(objectify.ObjectifiedElement):

    # TODO: Implementar metodo para mostrar atributos filhos

    def __getattr__(self, item):
        if item in NAO_OBRIGATORIO:
            return VoidElement()

        if self.tag.endswith('ICMS') or self.tag.endswith('IPI'):
            for child in self.getchildren():
                if 'ICMS' in child.tag or 'IPI' in child.tag:
                    search = re.search('{.*}(.*)', child.tag)
                    if not search:
                        continue
                    tag = search.group(1)
                    return getattr(self, tag)

        # Caso o atributo solicitado não exista, é buscado no danfe_formatado
        # um metodo que possa retornar o valor desse atributo
        if 'nfe' in self.tag:
            if hasattr(danfe_formata, item):
                result = eval(
                    'danfe_formata.' + item + '(self)')
                return result
            else:
                raise AttributeError
        else:
            raise AttributeError

    def __getattribute__(*args):
        result = objectify.ObjectifiedElement.__getattribute__(*args)

        # Caso existe um metodo de formatação para o atributo no danfe_formatado
        if type(result) == NFeElement:
            search = re.search('{.*}(.*)', result.tag)
            if not search:
                return result
            tag = search.group(1)
            method = ('formata_%s' % tag)
            if hasattr(danfe_formata, method):
                result = eval(
                    'danfe_formata.' + method + '(\'' + str(result.text) + '\')')

        return result
