import easySQL.tables
import easySQL.types, easySQL.exceptions


@easySQL.tables.Table(drop_on_create=True)
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
            "json": easySQL.types.JSON,
            "completed": easySQL.types.CHOICE
        }

foods_table = FoodsTable()
print(foods_table)

foods_table.insert_row(('orange', 3, 'fruit', {'sugar': '50g'}, 'yes'))
foods_table.insert_row(('apple', 2, 'fruit', {'sugar': '20g'}, 'yes'))
foods_table.insert_row(('banana', 5, 'fruit', {'sugar': '10g'}, 'no'))


rows = foods_table.fetch() # fetches all
print(rows)
rows2 = foods_table.fetch(entries=2) # fetches many
print(rows2)
rows3 = foods_table.fetch(entries=1) # fetches one
print(rows3)
