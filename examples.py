import easySQL
import easySQL.tables
import easySQL.types


@easySQL.tables.Table(initCreate=True, drop_on_create=True)
class FoodsTable:
    """ A example table using easySQL and its TypeComplex;
    """
    path_to_database = "test.sqlite"
    name: str = "Foods"
    columns: dict[str, easySQL.types.TypeComplex] = {
            "id": easySQL.types.BASIC_PRIMARY_KEY,
            "name": easySQL.types.TypeComplex('string', isUnique=True),
            "qty": easySQL.types.INTEGER,
            "type": easySQL.types.STRING
        }

foods_table = FoodsTable()
print(foods_table.__class__)