# -*- coding: utf-8 -*-
from pysvg.core import *

def getXML(self):
    """
    Return a XML representation of the current element.
    This function can be used for debugging purposes. It is also used by getXML in SVG

    @return:  the representation of the current element as an xml string
    """
    xml = u'<' + unicode(self._elementName) + u' '
    for key,value in self._attributes.items():
        if value != None:
            xml += unicode(key) + '="' + self.quote_attrib(unicode(str(value))) + u'" '
    if len(self._subElements) == 0:
        xml += u' />\n'
    else:
        xml += u' >\n'
        for subelement in self._subElements:
            xml += unicode(subelement.getXML())
        xml += u'</'+unicode(self._elementName) + u'>\n'
    return xml

def wrap_xml(self, xml, encoding='ISO-8859-1', standalone='no'):
    """
    Method that provides a standard svg header string for a file
    """
    header = u'''<?xml version="1.0" encoding="%s" standalone="%s"?>''' % (encoding, standalone)
    header = header.encode("utf-8")
    return header + xml

def save(self, filename, encoding='ISO-8859-1', standalone='no'):
    """
    Stores any element in a svg file (including header).
    Calling this method only makes sense if the root element is an svg elemnt
    """
    f = open(filename, 'w')
    xml = self.getXML()
    xml = xml.encode("utf-8")
    f.write(self.wrap_xml(xml, encoding, standalone))
    f.close()

BaseElement.getXML = getXML
BaseElement.wrap_xml = wrap_xml
BaseElement.save = save
