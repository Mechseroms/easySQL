from dataclasses import dataclass
import json
from .exceptions import ValidationFailed
from typing import Annotated

@dataclass
class TypeComplex:
    """ Creates a SQL string based on its set parameters for ease of use.
    type arg: can be 'string', 'integer', 'bool', 'real', 'blob'
    """
    type: str # can be string, integer, bool, real, blob
    isPrimaryKey: bool = False
    isUnique: bool = False
    isAutoIncremental: bool = False
    useDefault: bool = False
    default: any = None

    def normalize(self):
        string = f"{self.type} {'UNIQUE ' if self.isUnique else ''}{'PRIMARY KEY ' if self.isPrimaryKey else ''}{'AUTOINCREMENT' if self.isAutoIncremental else ''}"
        return string.strip()
    
    def validate(self, data, column_name: str = "Unknown"):
        if data:
            return True
        elif self.useDefault:
            return self.default
        else:
            print(data)
            raise ValidationFailed(column_name)
    
    def pack(self,data):
        """ packs the data for insertion into database """
        return data
    
    def unpack(self, data):
        """ unpacks the data for fetching from database """
        return data

    def validate_and_pack(self, data, column_name: str = "Unknown"):
        if self.validate(data, column_name=column_name): return self.pack(data)

class DictionaryComplex(TypeComplex):
    def unpack(self, data: str) -> dict:
        tag = "\\j*s*o*n\\"
        data = data.replace(tag, "")
        data: dict = json.loads(data)
        return data
    
    def pack(self, data: dict) -> str:
        tag = "\\j*s*o*n\\"
        data: str = json.dumps(data)
        data = data + tag
        return data.replace('"', '\"')
    
    def validate(self, data, column_name: str = "unknown"):
        if isinstance(data, dict):
            return True
        else:
            raise ValidationFailed(column_name)

class ListComplex(TypeComplex):
    def unpack(self, data: str) -> dict:
        tag = "\\j*s*o*n\\"
        data = data.replace(tag, "")
        data: dict = json.loads(data)
        return data
    
    def pack(self, data: dict) -> str:
        tag = "\\j*s*o*n\\"
        data: str = json.dumps(data)
        data = data + tag
        return data.replace('"', '\"')
    
    def validate(self, data, column_name: str = "Unknown"):
        if isinstance(data, list):
            return True
        else:
            raise ValidationFailed(column_name)


class JSONTypeComplex(TypeComplex):
    def pack(self, data: list | dict | str):
        return json.dumps(data)
    
    def unpack(self, data: str):
        return json.loads(data)

class ChoiceComplex(TypeComplex):
    def __init__(self, type, choices=['yes', 'no'], useDefault=False, default=None):
        super().__init__(type=type, useDefault=useDefault, default=default)
        self.choices = choices

    def validate(self, data, column_name: str = "Unknown"):
        if data in self.choices:
            return True
        else:
            raise ValidationFailed(column_name)
        
STRING = TypeComplex(type='string', useDefault=True, default='')
STRING.__doc__ = "This is a basic TypeComplex to create a column in SQL that expects a string type."

INTEGER = TypeComplex(type='integer', useDefault=True, default=0)
INTEGER.__doc__ = "This is a basic TypeComplex to Create a column in SQL that expects a integer type."

def validate(data, column_name: str = "Unknown"):
    if data or str(data) == "0":
            return True
    else:
        raise ValidationFailed(column_name)
    
INTEGER.validate = validate

ID = TypeComplex(type='integer', isPrimaryKey=True, isAutoIncremental=True)
ID.__doc__ = "This TypeComplex creates an Auto Incrementing Primary Key Integer often refered to as ID in many tables."

JSON = JSONTypeComplex(type='string', useDefault=True, default='') # TODO: create a function for converting lists and dict into json string and back

CHOICE = ChoiceComplex(type="string", useDefault=True, default='')

DICTIONARY = DictionaryComplex(type="string")
LIST = ListComplex(type="string")