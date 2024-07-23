__version__ = '1.2.1'

from lxml import etree
from lxml import objectify

lookup = etree.ElementNamespaceClassLookup(
    objectify.ObjectifyElementClassLookup())
parser = etree.XMLParser()
parser.set_element_class_lookup(lookup)

# Não troque essa ordem ou tire isso daqui que vai dar merda!
from erpbrasil.edoc.pdf import nfe  # noqa: F401,F403,E402
from erpbrasil.edoc.pdf.base import ImprimirXml  # noqa: F401,F403,E402
