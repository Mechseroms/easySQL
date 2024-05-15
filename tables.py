from typing import Any
import sqlite3, pathlib, csv
from collections import namedtuple
from .exceptions import ImproperPath

def SQLiteTable(initCreate: bool = True, drop_on_create: bool = False):
    """Decorates a class to be a table; 3 arguments must be assigned in the Class block:
    path_to_database, name, columns.

    Args:
        initCreate (bool, optional): _description_. Defaults to True.
        drop_on_create (bool, optional): _description_. Defaults to False.
        path_to_database str:
        name str: name of the table in the database
        columns dict[str, TypeComplex]: A dictionary with the keys representing the columns in the database and the value a TypeComplex.
    """
    def wrapper(cls):
        if isinstance(cls.path_to_database, (pathlib.Path, str)) is False: raise ImproperPath(cls.path_to_database)
        class SQLITETable(cls):
            def __init__(self, *args, **kwargs) -> None:
                self.name = cls.name
                self.columns = cls.columns
                if initCreate: self.initCreate = initCreate
                
                self.parsed_non_auto_columns = {
                    k: v for k, v in self.columns.items() if not v.isAutoIncremental
                    }
                
                self.path_to_database = cls.path_to_database
                self.data_object = namedtuple(f"{self.name}_row", list(self.columns.keys()))
                self.columns_validation = len([column for column, type in self.columns.items() if not type.isPrimaryKey])
                
                if initCreate: self.create_table(drop=drop_on_create)

            def __repr__(self) -> str:
                return f"{self.__class__.__name__} ('{self.name}'@'{self.path_to_database}')"

            def connect(self) -> sqlite3.Connection:
                """ Returns the database specific to this table."""
                if isinstance(cls.path_to_database, pathlib.Path):
                    return sqlite3.connect(database=cls.path_to_database.absolute())
                if isinstance(cls.path_to_database, str):
                    return sqlite3.connect(database=cls.path_to_database)
            
            @property
            def _create_sql(self) -> str:
                sql_command_string = ', '.join(
                        [f"{column_name} {column_type.normalize()}" for column_name, column_type in self.columns.items()]
                        )
                return f"CREATE TABLE {self.name} ({sql_command_string});" 

            @property
            def _drop_sql(self) -> str:
                return f"DROP TABLE {self.name};"

            @property
            def _insert_sql(self) -> str:
                column_denotation = ', '.join(
                    [f"{column_name}" for column_name, column_type in self.columns.items() if not column_type.isAutoIncremental]
                    )
                values_denotaion = ', '.join(
                    [f"?" for column_type in self.columns.values() if not column_type.isAutoIncremental]
                    )
                    
                return f"({column_denotation}) VALUES ({values_denotaion})"

            def _select_sql(self, column: str = None, match = None) -> str:
                if column:
                    return f"SELECT * FROM {self.name} WHERE {column}= '{match}'"
                else:
                    return f"SELECT * FROM {self.name}"
            
            def validate(self, value):
                if isinstance(value, str):
                    value = value.replace("'", "**&**")
                return value
            
            def devalidate(self, value):
                if isinstance(value, str):
                    value = value.replace("**&**", "'")
                return value

            def _update_SQL(self, data: dict, id: str) -> str:
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
                    middle_string = ""
                    current_count = 0
                    for key, value in data.items():
                        if current_count == len(data.items())-1:
                            middle_string += f" {key} = '{self.validate(value)}'"
                        else:
                            middle_string += f" {key} = '{self.validate(value)}', "
                        current_count += 1
                    return middle_string
                return f"UPDATE {self.name} SET{manufactur_update_SQL_string(data)} WHERE id = {id}"

            def create_table(self, drop: bool = False) -> None:
                if drop:
                    self.drop_table()
                try:
                    with self.connect() as database:
                        cursor = database.cursor()            
                        cursor.execute(self._create_sql)
                except sqlite3.OperationalError as e:
                    print(e)   
            
            def drop_table(self) -> tuple[bool, Exception | None]:
                try:
                    with self.connect() as database:
                        cursor = database.cursor()            
                        cursor.execute(self._drop_sql)
                    return True, None
                except sqlite3.OperationalError as error:
                    return False, error

            def fetch(self, *, filter: tuple[str, Any] = None, convert_data=True, entries: int = 0) -> list:
                
                if filter:
                    query = self._select_sql(column=filter[0], match=filter[1])
                else:
                    query = self._select_sql()

                with self.connect() as database:
                    cursor = database.cursor()
                    cursor.execute(query)

                    if entries > 1:
                        batch = cursor.fetchmany(size=entries)

                    if entries == 1:
                        item = cursor.fetchone()

                        if item != None:
                            batch = [item]
                        else:
                            batch = []

                    if entries == 0:
                        batch = cursor.fetchall()
                    
                    batch = self.unpack_data(rows=batch)
                    # TODO:: this is where we need to actually column_type.unpack the data by types
                    if not convert_data:
                        return batch
                    
                    return self.convert_data(batch)

            def insert_row(self, data: tuple):
                query = namedtuple('Query', ['query', 'data'])
                if len(data) == self.columns_validation:
                    packed_data = [self.validate(column_type.validate_and_pack(data[i])) for i, column_type in enumerate(self.parsed_non_auto_columns.values())]
                    query = query(query=f"INSERT INTO {self.name}{self._insert_sql}", data=tuple(packed_data))
                else:
                    query = query(query=False, data= f"passed data to {self.name} is not the right length of entries")

                assert query.query, query.data
                with self.connect() as database:
                    cursor = database.cursor()
                    cursor.execute(query.query, query.data)

            def unpack_data(self, rows):
                new_rows = []
                for row in rows:
                    new_rows.append([column_type.unpack(self.devalidate(row[i])) for i, column_type in enumerate(self.columns.values())])
                return new_rows

            def pack_data(self, data):
                new_data = {}
                for key, value in data.items():
                    new_data[key] = self.columns[key].pack(value)
                return new_data

            def convert_data(self, rows: list) -> Any:
                """ Takes rows returned by the tables SQL_select string and returns them as namedtuples.

                Args:
                    rows (listortuple): 

                Returns:
                    (listortuple): returns a list of namedtuple.
                """
                self.keys = list(self.columns.keys())
                return [self.data_object(**{key: data[i] for i, key in enumerate(self.keys)}) for data in rows]
            
    
            def update_table_row_by_id(self, id: int, data: dict):
                data = self.pack_data(data)
                query = self._update_SQL(data=data, id=id)
                print(query)
                with self.connect() as database:
                    cursor = database.cursor()       
                    cursor.execute(query)
            
            def export_csv(self, filepath: pathlib.Path):
                rows = self.fetch(convert_data=False)
                print(rows)
                with filepath.open('w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(self.columns.keys())
                    csvwriter.writerows(rows)
                    

        
        
        return SQLITETable
    return wrapper