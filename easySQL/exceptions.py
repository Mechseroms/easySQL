class ImproperPath(Exception):
    def __init__(self, path_to_database):
        self.message = f"{type(path_to_database)}: {path_to_database}; path to database must be a pathlib.Path object or a str pointing to the database path..."
        super().__init__(self.message)