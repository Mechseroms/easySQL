# easySQL
An easy sqlite3 interface for basic functioning where data fetched is returned as NamedTuples for out of the box interfaces to your data.

I really made this as I had found that I liked to interface with SQlite databases for my small amounts of data for readablity. Well this forced me to rewrite alot of code over and over, so after starting to learn about decorators I set out to develop an easy to use interface that takes writing SQL code that i found tedious into simple functions. This made developing a table as easy as instatiating a decorated class.

## Usage
EasySQL relies on the use of the `@easySQL.Table` decorator with the argument; `path_to_database`. You create a class that instantiates with the variables `self.name` a string identifying the table and `self.columns` a dictionary of key value pairs in the format of column_name: value_type.

The value types can be one or a combo of the following types. These can be combined with the "+" operator or the "and" operator:

* `easySQL.STRING`: a basic string.
* `easySQL.INTEGER`: a basic integer.
* `easySQL.UNIQUE`: causes the value to have to be enforced to a unique entry in the database table.
* `easySQL.PRIMARY_KEY`: causes the value to be the primary key in the database table.
* `easySQL.JSON`: serializes a list or dictionary into a string to be inserted and selected from the database table.

Below is an example of easySQL at its current state:

```python
import easySQL

@easySQL.Table(path_to_database="test.sqlite")
class MyTable:
    """ A example table using easySQL and its TypeComplexes;
    """
    def __init__(self) -> None:
        self.name = "foo"
        self.columns = {
            "id": easySQL.BASIC_PRIMARY_KEY,
            "foo": easySQL.TypeComplex('string', isUnique=True),
            "duh": easySQL.INTEGER
        }

my_table = MyTable()

```
