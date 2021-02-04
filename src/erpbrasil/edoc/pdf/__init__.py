from lxml import etree
from lxml import objectify

__version__ = '0.2.0'

lookup = etree.ElementNamespaceClassLookup(
    objectify.ObjectifyElementClassLookup())
parser = etree.XMLParser()
parser.set_element_class_lookup(lookup)
