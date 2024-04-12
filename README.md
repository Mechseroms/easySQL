# easySQL
An easy sqlite3 interface for basic functioning where data fetched is returned as NamedTuples for out of the box interfaces to your data.

I really made this as I had found that I liked to interface with SQlite databases for my small amounts of data for readablity. Well this forced me to rewrite alot of code over and over, so after starting to learn about decorators I set out to develop an easy to use interface that takes writing SQL code that i found tedious into simple functions. This made developing a table as easy as instatiating a decorated class.

## Usage
EasySQL relies on the use of the `@easySQL.tables.Table` decorator with the argument; `path_to_database`. You create a class that instantiates with the variables `self.name` a string identifying the table and `self.columns` a dictionary of key value pairs in the format of column_name: value_type.

* `easySQL.types.STRING`: a basic string.
* `easySQL.types.INTEGER`: a basic integer.
* `easySQL.types.ID`: causes the value to be the primary key in the database table.
* `easySQL.types.JSON`: serializes a list or dictionary into a string to be inserted and selected from the database table.

Below is an example of easySQL at its current state at its bare minimum:

```python
import easySQL

@easySQL.tables.Table()
class FoodsTable:
    """ A example table using easySQL and its TypeComplex;
    """
    path_to_database = "test.sqlite"
    name: str = "Foods"
    columns: dict[str, easySQL.types.TypeComplex] = {
            "id": easySQL.types.ID,
            "name": easySQL.types.TypeComplex('string', isUnique=True),
            "qty": easySQL.types.INTEGER,
            "type": easySQL.types.STRING,
            "json": easySQL.types.JSON
        }

```
As you can see this table will be created with the name "Foods" and a series of columns. I have shown the basic use
of the `easySQL.types.TypeComplex` object which is the building blocks of how the table interacts with your data. In this instance I created a name column that will be of the type string but also setting it to be unique so no two rows can have the same name in them.

easySQL.types.JSON is my basic implementation of a TypeComplex that transforms data at insertion to serialize a list or dictionary into a string. This is also easily replicated by overwriting a TypeComplex's `transfrom` method like so:
```python
from easySQL.types import TypeComplex
import json

def transform_json(data):
    return json.dumps(data)

mycomplex = TypeComplex('string')
mycomplex.transform = transform_json
```

Or with Lambda:
```python
from easySQL.types import TypeComplex
import json

mycomplex = TypeComplex('string')
mycomplex.transform = lambda data: json.dumps(data)
```
