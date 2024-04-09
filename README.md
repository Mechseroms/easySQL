# easySQL
An easy sqlite3 interface for basic functioning where data fetched is returned as NamedTuples for out of the box interfaces to your data.

I really made this as I had found that I liked to interface with SQlite databases for my small amounts of data for readablity. Well this forced me to rewrite alot of code over and over, so after starting to learn about decorators I set out to develop an easy to use interface that takes writing SQL code that i found tedious into simple functions. This made developing a table as easy as instatiating a decorated class.

```python

import easySQL, pathlib

@easySQL.Table
Class MyTable:
    def __init__(self)
        self.name = "foo"
        self.columns = {
            "foo": easySQL.String,
            "duh": easySQL.INTEGER
            ...
        }

easySQL.intergrate(pathlib.Path('test.sqlite'))

my_table = MyTable()

easySQL.create_table(my_table, drop=False)
```
