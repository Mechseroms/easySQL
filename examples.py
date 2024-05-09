from easySQL.types import ID, STRING
from easySQL.tables import SQLiteTable

# TODO: Need to add a row_count method to Table that returns a total count from the table
# TODO: Need to add a raw_query method to be able to pass a custom query and return all rows
#       Fetch statement essentially but with a SQL string passed in.

@SQLiteTable(drop_on_create=True)
class MyTable:
    path_to_database = "test.sqlite"
    name = "test"
    columns = {
        "id": ID,
        "name": STRING,
        "type": STRING
    }

my_table = MyTable()

# Inserting data into a table, data is inserted into tables as a tuple of all the columns data in order.
# single column tables as our table must have a following comma to ensure strings are represented as a single column and
# not split.
row_data: tuple = ("Apple", "Fruit")
my_table.insert_row(row_data)

row_data: tuple = ("Apple", "Veggie")
my_table.insert_row(row_data)

row_data: tuple = ("Orange", "Fruit")
my_table.insert_row(row_data)

row_data: tuple = ("Banana", "Fruit")
my_table.insert_row(row_data)

# Fetching data from a table. 
# You can pass the convert_data = False argument to fetch in order to stop the table
# from converting the rows into the tables data_object in the form of a named tuple. 
# these namedtuples will be constructed using the tables name which will allow for easier 
# identification of what table what objects are returned from.


# You can also pass a filter into fetch to filter by a single column.

# calling the fetch method will return all rows from the table
rows = my_table.fetch()

# to fetch many or one you would pass an int of the amount of entries you would like from that table
rows = my_table.fetch(entries=1)

# using the filter argument; this is passed as a tuple with two values, the column name in the form of a string, and
# the value you would like returned.
filter: tuple = ('id', 2)
rows = my_table.fetch(filter=filter, entries=1)

print(rows) # -> [test_row(id=2, name='Orange')]

filter: tuple = ('name', 'Apple')
rows = my_table.fetch(filter=filter)

print(rows) # -> [test_row(id=1, name='Apple')] 

# since rows are returned as namedtuples they are open to property calls.

print(rows[1].name) # -> "Apple"
