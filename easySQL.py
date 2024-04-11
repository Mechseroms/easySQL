from typing import Any
import sqlite3, pathlib
from collections import namedtuple
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


def VALDATED_STRING():
    return 'string'

class ImproperPath(Exception):
    def __init__(self, path_to_database):
        self.message = f"{type(path_to_database)}: {path_to_database}; path to database must be a pathlib.Path object or a str pointing to the database path..."
        super().__init__(self.message)


def Table(path_to_database: pathlib.Path | str, *, 
          initCreate: bool = True,
          drop_on_create=False):
    """ easySQL decorator for table classes for easy instantiation of many of the SQL_execute strings.

    This class will always need these variables defined within its __init__ method;

    self.name = "foo";  This will be the name of the table in the integrated database
    self.columns = {foo: dah, ...}; dictionary of foo being the column name, and dah being the columns type in the database
        types for a column are:
            - STRING
            - INTEGER
            - JSON
            - TypeComplex

    Returns:
        Table: returns a Table class wrapped around the original class.
    """
    if isinstance(path_to_database, (pathlib.Path, str)) is False: raise ImproperPath(path_to_database)
    
    def wrapper(cls):
        class Table(cls):
            def __init__(self, *args, **kwargs) -> None:
                super(Table, self).__init__(*args, **kwargs)
                self.path_to_database = path_to_database
                self.data_object = namedtuple(f"{self.name}_row", list(self.columns.keys()))
                self.columns_validation = len([column for column, type in self.columns.items() if not type.isPrimaryKey])
                print(self.name)
                if initCreate: self.create_table(drop=drop_on_create)

            def __repr__(self):
                return f"{self.__class__.__name__} ('{self.name}'@'{self.path_to_database}')"

            def connect(self):
                """ Returns the database specific to this table."""
                if isinstance(path_to_database, pathlib.Path):
                    return sqlite3.connect(database=path_to_database.absolute())
                if isinstance(path_to_database, str):
                    return sqlite3.connect(database=path_to_database)
            
            @property
            def _create_sql(self) -> str:
                sql_command_string = ', '.join(
                        [f"{column_name} {column_type.normalize()}" for column_name, column_type in self.columns.items()]
                        )
                return f"CREATE TABLE {self.name} ({sql_command_string});" 

            @property
            def _drop_sql(self):
                return f"DROP TABLE {self.name};"

            @property
            def _insert_sql(self):
                column_denotation = ', '.join(
                    [f"{column_name}" for column_name, column_type in self.columns.items() if not column_type.isAutoIncremental]
                    )
                values_denotaion = ', '.join(
                    [f"?" for column_type in self.columns.values() if not column_type.isAutoIncremental]
                    )
                    
                return f"({column_denotation}) VALUES ({values_denotaion})"


            def create_table(self, drop: bool = False):
                if drop:
                    self.drop_table()
                try:
                    with self.connect() as database:
                        cursor = database.cursor()            
                        cursor.execute(self._create_sql)
                except sqlite3.OperationalError as e:
                    print(e)   
            
            def drop_table(self):
                try:
                    with self.connect() as database:
                        cursor = database.cursor()            
                        cursor.execute(self._drop_sql)
                except sqlite3.OperationalError:
                    pass

            def _select_sql(self, column: str = None, match = None):
                if column:
                    return f"SELECT * FROM {self.name} WHERE {column}= '{match}'"
                else:
                    return f"SELECT * FROM {self.name}"
        
            def fetchone_from_table(self, filter: tuple[str,  Any] = None, convert_data=True):
                if filter:
                    query = self._select_sql(column=filter[0], match=filter[1])
                else:
                    query = self._select_sql()
                
                with self.connect() as database:
                    cursor = database.cursor()
                    cursor.execute(query)

                    if not convert_data:
                        return cursor.fetchone()
                
                return self.convert_data(cursor.fetchone())

            def insert_row(self, data: tuple):
                query = namedtuple('Query', ['query', 'data'])
                if len(data) == self.columns_validation:
                    query = query(query=f"INSERT INTO {self.name}{self._insert_sql}", data=data)
                else:
                    query = query(query=False, data= f"passed data to {self.name} is not the right length of entries")

                assert query.query, query.data
                with self.connect() as database:
                    cursor = database.cursor()
                    cursor.execute(query.query, query.data)

            def update_row_by_id(self, data: dict, id: str):
                """ Update a row at {id} with {data}.

                Args:
                    data (dict): key = column, value = data to update to
                    id (str): row_id in Table
                """
                def manufactur_update_SQL_string(data: dict) -> str:
                    """ takes data and builds a SQL_execute string segment

                    Args:
                        data (dict): Key = column, value = data to update to

                    Returns:
                        _type_: middle segment of SQL_execute string
                    """
                    # TODO: this is a very crude implementtion
                    middle_string = ''
                    current_count = 0
                    for key, value in data.items():
                        if current_count == len(data.items())-1:
                            middle_string += f" {key} = '{value}'"
                        else:
                            middle_string += f" {key} = '{value}', "
                        current_count += 1
                    return middle_string
                return f"UPDATE {self.name} SET{manufactur_update_SQL_string(data)} WHERE id = {id}"

            def convert_data(self, rows: list | tuple) -> Any:
                """ Takes rows returned by the tables SQL_select string and returns them as namedtuples.

                Args:
                    rows (listortuple): 

                Returns:
                    (listortuple): returns a list of namedtuple.
                """
                self.keys = list(self.columns.keys())
                if isinstance(rows, list):
                    return [self.data_object(**{key: data[i] for i, key in enumerate(self.keys)}) for  data in rows]
                if isinstance(rows, tuple):
                    return [self.data_object(**{key: rows[i] for i, key in enumerate(self.keys)})][0]
            
            
        return Table
    return wrapper
    
def update_table_row_by_id(table: Table, row):
    query = table.update_row_by_id(data=row[1], id=row[0])
    with table.get_database() as database:
        cursor = database.cursor()            
        cursor.execute(query)
    
def fetchall_from_table(table, filter: tuple[str, Any] = None, convert_data=True) -> list:
    """ Fetches all rows from the database using passed query

    Args:
        query (str): SQL_execute string

    Returns:
        list: list of rows as tuples
    """

    if filter:
        query = table.select_row(column=filter[0], match=filter[1])
    else:
        query = table.select_row()

    with table.get_database() as database:
        cursor = database.cursor()
        cursor.execute(query)
        batch = cursor.fetchall()
        
        if len(batch) == 1:
            batch = batch[0]

        if not convert_data:
            return batch
        
        return table.convert_data(batch)