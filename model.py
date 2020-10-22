from typing import ValuesView


class PropertyAsset(object):
    def __init__(self, title, description):
        self.title = title or None
        self.description = description or None

class PropertySet(PropertyAsset):
    def __init__(self, title, description, id=None, version=None):
        super().__init__(title, description)
        self.id = id
        self.version = version
        self.properties = []

    def addproperty(self, prop):
        self.properties.append(prop)
    
    def toJSON(self):
        props = {}
        for prop in self.properties:
            props[prop.title] = prop
        
        return { "$id":self.id,
                 "$schema":"http://json-schema.org/draft-07/schema#",
                 "ifcversion":self.version,
                 "type":"object",
                 "title":self.title, 
                 "description":self.description,
                 "properties":props}


class Property(PropertyAsset):
    def __init__(self, title, description, datatype = None):
        super().__init__( title, description)
        self.datatype = datatype
    @staticmethod
    def matchtype(name):
        raise Error("subclass responsibility")
    def toJSON(self):
        json = {"title":self.title,
        "description":self.description}
        if self.datatype:
            json['datatype'] = self.datatype
        return json


class SingleValueType(Property):
    @staticmethod
    def matchtype(name):
        return name == "TypePropertySingleValue" or name == "TypePropertyBoundedValue"
    def toJSON(self):
        json = super().toJSON()
        json['type'] = 'string'
        return json

class CollectionType(Property):
    def __init__(self, values):
        super().__init__(None, None)
        self.values = values
    def toJSON(self):
        json = super().toJSON()
        json['type'] = 'string'
        return json

class EnumType(CollectionType):
    @staticmethod
    def matchtype(name):
        return name == "TypePropertyEnumeratedValue"
    def toJSON(self):
        json = super().toJSON()
        json['enum'] = self.values
        return json

class ArrayType(CollectionType):
    @staticmethod
    def matchtype(name):
        return name == "TypePropertyListValue"

    def toJSON(self):
        json = super().toJSON()
        json['type'] = 'array'
        json['items'] = self.values
        return json
        
class TableType(CollectionType):
    @staticmethod
    def matchtype(name):
        return name == "TypePropertyTableValue"
    def toJSON(self):
        json = super().toJSON()
        json['type'] = 'object'
        return json

class ReferenceType(Property):
    @staticmethod
    def matchtype(name):
        return name == "TypePropertyReferenceValue"
    def toJSON(self):
        json = super().toJSON()
        return json
