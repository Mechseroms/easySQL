import easySQL, sys

@easySQL.Table(path_to_database="test.sqlite", initCreate=True, drop_on_create=True)
class FoodsTable:
    """ A example table using easySQL and its TypeComplex;
    """
    def __init__(self) -> None:
        self.name: str = "Foods"
        self.columns: dict[str, easySQL.TypeComplex] = {
            "id": easySQL.BASIC_PRIMARY_KEY,
            "name": easySQL.TypeComplex('string', isUnique=True),
            "qty": easySQL.INTEGER,
            "type": easySQL.STRING
        }

food_table = FoodsTable()
foods = [("apple", 23, "fruit"),("banana", 5, "fruit"),("hamburger", 2, "meat"),("milk", 1, "dairy")]

for food in foods:
    food_table.insert_row(food)

food = food_table.fetchone_from_table(("id", 4))

print(food.name)