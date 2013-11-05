class Dialect:
    def __init__(self, has_header_row=False, **kwargs):
        self.has_header_row = has_header_row
        self.csv_dialect = kwargs
        self.columns = []

    def add_column(self, column):
        self.columns.append(column)

    def finalize(self):
        self.columns.sort(key=lambda column: column.counter)

