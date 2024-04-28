# easySQL
An easy sqlite3 interface for basic functioning where data fetched is returned as NamedTuples for out of the box interfaces to your data.

I really made this as I had found that I liked to interface with SQlite databases for my small amounts of data for readablity. Well this forced me to rewrite alot of code over and over, so after starting to learn about decorators I set out to develop an easy to use interface that takes writing SQL code that i found tedious into simple functions. This made developing a table as easy as instatiating a decorated class.

## Usage
EasySQL relies on the use of the `@easySQL.tables.Table` decorator. You create a class that instantiates with the variables `path_to_database`, `name` a string identifying the table and `columns` a dictionary of key value pairs in the format of column_name: value_type.

* `easySQL.types.STRING`: a basic string.
* `easySQL.types.INTEGER`: a basic integer.
* `easySQL.types.ID`: causes the value to be the primary key in the database table.
* `easySQL.types.JSON`: serializes a list or dictionary into a string to be inserted and selected from the database table.
* `easySQL.types.CHOICE: a default choice column that validates data to be 'yes' or 'no'

Below is an example of easySQL at its current state at its bare minimum:

### Creating a Table
You create a table by decorating a class with the SQLiteTable decorator. Within this class you must have the variables `path_to_database`, `name`, and `columns` defined for the table. From there just instantiate the class into a variable as you see fit.

```python
from easySQL.types import ID, STRING
from easySQL.tables import SQLiteTable

@SQLiteTable()
class MyTable:
    path_to_database = "test.sqlite"
    name = "test"
    columns = {
        "id": ID,
        "name": STRING
    }

my_table = MyTable()
```

### Inserting data into a table
Inserting data into a table, data is inserted into tables as a tuple of all the columns data in order.
single column tables as our table must have a following comma to ensure strings are represented as a single column and
not split.

```python
row_data: tuple = ("Apple",)
my_table.insert_row(row_data)
```

### Fetching data from a table. 
You can pass the convert_data = False argument to fetch in order to stop the table
from converting the rows into the tables data_object in the form of a named tuple. 
these namedtuples will be constructed using the tables name which will allow for easier 
identification of what table what objects are returned from.

```python
# calling the fetch method will return all rows from the table
rows = my_table.fetch()

# to fetch many or one you would pass an int of the amount of entries you would like from that table
rows = my_table.fetch(entries=4)

# using the filter argument; this is passed as a tuple with two values, the column name in the form of a string, and
# the value you would like returned.
filter: tuple = ('id', 5)
rows = my_table.fetch(filter=filter)

print(rows) # -> [test_row(id=5, name='Apple')]

filter: tuple = ('name', 'Apple')
rows = my_table.fetch(filter=filter)

print(rows) # -> [test_row(id=1, name='Apple'), test_row(id=2, name='Apple'), test_row(id=3, name='Apple')] 

# since rows are returned as namedtuples they are open to property calls.

print(rows[1].name) # -> "Apple"
```

## TypeComplexes
The backend of easySQL is its types and what I have called TypeComplexes, dont ask me why I named them that, which holds the tables ability to construct
all the neccessary SQL strings to interact with the database. I have listed the types included with easySQL above, but to create your own you simply can do so by importing the TypeComplex and initiating or subclassing your own. From there you can overwrite any of its methods; pack, unpack, validate.

Here is my basic implementation of json and TypeComplexes in a few different ways.

Instantiation:
```python
from easySQL.types import TypeComplex
import json

def dump_json(data):
    return json.dumps(data)

def load_json(data):
    return json.loads(data)

mycomplex = TypeComplex('string')
mycomplex.pack = dump_json
mycomplex.unpack = load_json
```

Or with Lambda:
```python
from easySQL.types import TypeComplex
import json

mycomplex = TypeComplex('string')
mycomplex.pack = lambda data: json.dumps(data)
mycomplex.unpack = lambda data: json.loads(data)
```

or with Subclassing:
```python
from easySQL.types import TypeComplex
import json

class JSONComplex(TypeComplex):
    def pack(data):
        return json.dumps(data)

    def unpack(data):
        return json.loads(data)
    
    def validate(data):
        if isinstance(data, [list, dict]):
            return True
        return False
```