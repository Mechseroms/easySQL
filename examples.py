import easySQL
import easySQL.tables
import easySQL.types, easySQL.exceptions


@easySQL.tables.Table
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

foods_table = FoodsTable()
print(foods_table)