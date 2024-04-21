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

    def normalize(self):
        string = f"{self.type} {'UNIQUE ' if self.isUnique else ''}{'PRIMARY KEY ' if self.isPrimaryKey else ''}{'AUTOINCREMENT' if self.isAutoIncremental else ''}"
        return string.strip()
    
    def validate(self, data):
        if data:
            return True
        else:
            print(self, data)
            raise ValidationFailed

    def transform(self, data):
        return data

    def validate_and_transform(self, data):
        if self.validate(data): return self.transform(data)
                 
class JSONTypeComplex(TypeComplex):
    def transform(self, data: list | dict | str):
        return json.dumps(data)

class ChoiceComplex(TypeComplex):
    def validate(self, data):
        choices = ['In', 'Out']
        if data in choices:
            return True
        else:
            raise ValidationFailed
        
STRING = TypeComplex(type='string')
STRING.__doc__ = "This is a basic TypeComplex to create a column in SQL that expects a string type."

INTEGER = TypeComplex(type='integer')
INTEGER.__doc__ = "This is a basic TypeComplex to Create a column in SQL that expects a integer type."

def validate(data):
    if data or str(data) == "0":
            return True
    else:
        raise ValidationFailed
    
INTEGER.validate = validate

ID = TypeComplex(type='integer', isPrimaryKey=True, isAutoIncremental=True)
ID.__doc__ = "This TypeComplex creates an Auto Incrementing Primary Key Integer often refered to as ID in many tables."

JSON = JSONTypeComplex(type='string') # TODO: create a function for converting lists and dict into json string and back

CHOICE = ChoiceComplex(type="string")
