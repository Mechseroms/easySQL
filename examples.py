import easySQL


@easySQL.Table(path_to_database="test.sqlite")
class MyTable:
    def __init__(self) -> None:
        self.name = "foo"
        self.columns = {
            "id": easySQL.INTEGER and easySQL.PRIMARY_KEY,
            "foo": easySQL.STRING,
            "duh": easySQL.INTEGER
        }

my_table = MyTable()
print(my_table)

easySQL.create_table(my_table, drop=True)