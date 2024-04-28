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

# Inserting data into a table, data is inserted into tables as a tuple of all the columns data in order.
# single column tables as our table must have a following comma to ensure strings are represented as a single column and
# not split.
row_data: tuple = ("Apple",)
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