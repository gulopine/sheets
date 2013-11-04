import functools
import datetime
import decimal

class Column:
    """
    An individual column within a CSV file. This serves as a base for attributes
    and methods that are common to all types of columns. Subclasses of Column
    will define behavior for more specific data types.
    """

    def __init__(self, title=None, required=True):
        self.title = title
        self.required = required
        self._validators = [self.to_python]

    def attach_to_class(self, cls, name, dialect):
        self.cls = cls
        self.name = name
        self.dialect = dialect
        if self.title is None:
            # Check for None so that an empty string will skip this behavior
            self.title = name.replace('_', ' ')
        dialect.add_column(self)

    def to_python(self, value):
        """
        Convert the given string to a native Python object.
        """
        return value

    def to_string(self, value):
        """
        Convert the given Python object to a string.
        """
        return value

    # Not yet written about

    def validator(self, func):
        self._validators.append(functools.partial(func, self))
        return func

    def validate(self, value):
        """
        Validate that the given value matches the column's requirements.
        Raise a ValueError only if the given value was invalid.
        """
        for validate in self._validators:
            validate(value)


class StringColumn(Column):
    pass


class IntegerColumn(Column):
    def to_python(self, value):
        return int(value)


class FloatColumn(Column):
    def to_python(self, value):
        return float(value)


class DecimalColumn(Column):
    """
    A column that contains data in the form of decimal values,
    represented in Python by decimal.Decimal.
    """

    def to_python(self, value):
        try:
            return decimal.Decimal(value)
        except decimal.InvalidOperation as e:
            raise ValueError(str(e))


class DateColumn(Column):
    """
    A column that contains data in the form of dates,
    represented in Python by datetime.date.

    format
        A strptime()-style format string.
        See http://docs.python.org/library/datetime.html for details
    """

    def __init__(self, *args, format='%Y-%m-%d', **kwargs):
        super(DateColumn, self).__init__(*args, **kwargs)
        self.format = format

    def to_python(self, value):
        """
        Parse a string value according to self.format
        and return only the date portion.
        """
        if isinstance(value, datetime.date):
            return value
        return datetime.datetime.strptime(value, self.format).date()

    def to_string(self, value):
        """
        Format a date according to self.format and return that as a string.
        """
        return value.strftime(self.format)

