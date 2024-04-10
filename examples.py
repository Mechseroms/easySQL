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