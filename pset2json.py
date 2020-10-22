import bs4
import requests
from pathlib import Path
from glob import glob
from model import PropertySet, Property, SingleValueType, EnumType, ArrayType, ReferenceType, TableType
import json


### Getters ###
def getpset(path):
    """Given a pset path, return its XML content"""
    with open(path, "r", encoding='utf-8') as f:
        return bs4.BeautifulSoup(f.read(), "xml")  

def getfield(prop, field):
    """Attempt to fetch the text contents of an XML tag"""
    return prop.find(field).next if prop.find(field) else None

def getattr(dom, field, attr):
    """Attempt to fetch the contents of an XML tag attribute"""
    tag = dom.find(field)
    return tag.get(attr) if tag else None




### Core ###

def psets2jsons(source, target):
    """Convert all psets to their JSON Schema equivalents"""
    for xmlpath in source.glob('*.xml'):
        filename = xmlpath.name.replace('.xml', '.json');
        data = getpset(xmlpath)
        pset = pset2json(data, filename)
        yield (filename, json.dumps(pset.toJSON(), default = lambda o: o.toJSON(), indent=4))



def pset2json(data, xmlpath):
    """Build up a single PropertySet"""
    pset = PropertySet(getfield(data, "Name"),
                       getfield(data, "Definition"),
                       str(xmlpath),
                       getattr(data, "IfcVersion", "version"))
    for xmlprop in data.find_all("PropertyDef"):
        prop = handleprop(xmlprop)
        pset.addproperty(prop)
    return pset
    


def handleprop(xmlprop):
    """Build up a single Property"""
    typetag = xmlprop.find("PropertyType")
    prop = Property(getfield(xmlprop, "Name"), 
                    getfield(xmlprop, "Definition"))
    
    typename = typetag.contents[1].name
    if SingleValueType.matchtype(typename):
        prop.datatype = getattr(xmlprop, "DataType", "type")

    elif EnumType.matchtype(typename):
        values = [field.next for field in typetag.find_all("EnumItem")]
        enum = EnumType(values)
        prop.datatype = enum

    elif ArrayType.matchtype(typename):
        values = [field.next for field in typetag.find_all("EnumItem")]
        array = ArrayType(values)
        prop.datatype = array

    elif TableType.matchtype(typename):
        print("table values not yet supported. Continuing...")

    elif ReferenceType.matchtype(typename):
        print("reference values not yet supported. Continuing...")

    else:
        print("unhandled prop type: {}".format(typetag.next))

    return prop


                    

if __name__ == "__main__":
    source = (Path(__file__).parent / 'psets' / 'xml')
    target = (Path(__file__).parent / 'psets' / 'json')
    for (filename, pset) in psets2jsons(source, target):
        with open((target / filename).resolve(), "w") as f:
            f.write(pset)