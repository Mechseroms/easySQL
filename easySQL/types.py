from dataclasses import dataclass

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
    

STRING = TypeComplex(type='string')
INTEGER = TypeComplex(type='integer')
BASIC_PRIMARY_KEY = TypeComplex(type='integer', isPrimaryKey=True, isAutoIncremental=True)
JSON = 'string ' # TODO: create a function for converting lists and dict into json string and back

