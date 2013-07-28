import csv
from collections import OrderedDict

from sheets import options

__all__ = ['Row', 'Reader', 'Writer']

class RowMeta(type):
    def __init__(cls, name, bases, attrs):
        if 'Dialect' in attrs:
            # Filter out Python's own additions to the namespace
            items = attrs.pop('Dialect').__dict__.items()
            items = dict((k, v) for (k, v) in items if not k.startswith('__'))
        else:
            # No options were explicitly defined
            items = {}
        cls._dialect = options.Dialect(**items)
        
        for key, attr in attrs.items():
            if hasattr(attr, 'attach_to_class'):
                attr.attach_to_class(cls, key, cls._dialect)

    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()


class Row(metaclass=RowMeta):
    # Not yet written about

    def __init__(self, *args, **kwargs):
        column_names = [column.name for column in self._dialect.columns]
        
        # First, make sure the arguments make sense
        if len(args) > len(column_names):
            msg = "__init__() takes at most %d arguments (%d given)"
            raise TypeError(msg % (len(column_names), len(args)))
        
        for name in kwargs:
            if name not in column_names:
                raise TypeError("Got unknown keyword argument '%s'" % name)
        
        for i, name in enumerate(column_names[:len(args)]):
            if name in kwargs:
                msg = "__init__() got multiple values for keyword argument '%s'"
                raise TypeError(msg % name)
            kwargs[name] = args[i]

        # Now populate the actual values on the object
        for column in self._dialect.columns:
            try:
                value = column.to_python(kwargs[column.name])
            except KeyError:
                # No value was provided
                value = None
            setattr(self, column.name, value)

    errors = ()

    def is_valid(self):
        valid = True
        self.errors = []
        for column in self._dialect.columns:
            value = getattr(self, column.name)
            try:
                column.validate(value)
            except ValueError as e:
                self.errors.append(e)
                valid = False
        return valid

    @classmethod
    def reader(cls, file):
        return Reader(cls, file)

    @classmethod
    def writer(cls, file):
        return Writer(cls, file)


class Reader:
    def __init__(self, row_cls, file):
        self.row_cls = row_cls
        self.csv_reader = csv.reader(file, **row_cls._dialect.csv_dialect)
        self.skip_header_row = row_cls._dialect.has_header_row

    def __iter__(self):
        return self

    def __next__(self):
        # Skip the first row if it's a header
        if self.skip_header_row:
            self.csv_reader.__next__()
            self.skip_header_row = False
        
        return self.row_cls(*self.csv_reader.__next__())


class Writer:
    def __init__(self, row_cls, file):
        self.columns = row_cls._dialect.columns
        self._writer = csv.writer(file, row_cls._dialect.csv_dialect)
        self.needs_header_row = row_cls._dialect.has_header_row

    def writerow(self, row):
        if self.needs_header_row:
            values = [column.title.title() for column in self.columns]
            self._writer.writerow(values)
            self.needs_header_row = False
        values = [getattr(row, column.name) for column in self.columns]
        self._writer.writerow(values)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


