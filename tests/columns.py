import unittest
import datetime
import decimal

import sheets


class ColumnTests(unittest.TestCase):
    invalid_values = []
    
    def setUp(self):
        self.column = sheets.Column()
        self.string_value = 'value'
        self.python_value = 'value'

    def test_validation(self):
        try:
            self.column.validate(self.python_value)
        except ValueError as e:
            self.fail(str(e))

    def test_python_conversion(self):
        python_value = self.column.to_python(self.string_value)
        self.assertEqual(python_value, self.python_value)

    def test_string_conversion(self):
        string_value = str(self.column.to_string(self.python_value))
        self.assertEqual(string_value, self.string_value)

    def test_invalid_value(self):
        for value in self.invalid_values:
            try:
                value = self.column.to_python(value)
            except ValueError:
                # If it's caught here, there's no need to test anything else
                return
            self.assertRaises(ValueError, self.column.validate, value)


class StringColumnTests(ColumnTests):
    def setUp(self):
        self.column = sheets.StringColumn()
        self.string_value = 'value'
        self.python_value = 'value'


class IntegerColumnTests(ColumnTests):
    def setUp(self):
        self.column = sheets.IntegerColumn()
        self.string_value = '1'
        self.python_value = 1
        self.invalid_values = ['invalid']


class FloatColumnTests(ColumnTests):
    def setUp(self):
        self.column = sheets.FloatColumn()
        self.string_value = '1.1'
        self.python_value = 1.1
        self.invalid_values = ['invalid']


class DecimalColumnTests(ColumnTests):
    def setUp(self):
        self.column = sheets.DecimalColumn()
        self.string_value = '1.1'
        self.python_value = decimal.Decimal('1.1')
        self.invalid_values = ['invalid']


class DateColumnTests(ColumnTests):
    def setUp(self):
        self.column = sheets.DateColumn()
        self.string_value = '2010-03-31'
        self.python_value = datetime.date(2010, 3, 31)
        self.invalid_values = ['invalid', '03-31-2010']


class FormattedDateColumnTests(ColumnTests):
    def setUp(self):
        self.column = sheets.DateColumn(format='%m/%d/%Y')
        self.string_value = '03/31/2010'
        self.python_value = datetime.date(2010, 3, 31)
        self.invalid_values = ['invalid', '03-31-2010']


