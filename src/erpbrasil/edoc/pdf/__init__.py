__version__ = '0.1.1'

from lxml import objectify, etree

lookup = etree.ElementNamespaceClassLookup(
    objectify.ObjectifyElementClassLookup())
parser = etree.XMLParser()
parser.set_element_class_lookup(lookup)

from erpbrasil.edoc.pdf import nfe
from erpbrasil.edoc.pdf.base import ImprimirXml
