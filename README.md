Sheets: CSV <---> Objects
=========================

Python ships with a `csv` module that allows you to move data to and from comma-
separated data files. Sheets build on that to easily convert that data into
Python objects and back into files again. You can specify the structure of your
data files using Python classes

    import sheets

    class Friend(sheets.Row):
        name = sheets.Column()
        date_of_birth = sheets.DateColumn()

This class can then be used to interact with individual files.

    >>> import datetime
    >>> for f in Friend.reader(open('friends.csv')):
    ...     age = datetime.date.today() - f.date_of_birth
    ...     print('%s is %d years old' % (f.name, age.days / 365.25))
    ... 
    Alice is 30.23 years old
    Bob is 25.67 years old

You can also create records in Python and save them to the file.

    >>> friends = list(Friend.reader(open('friends.csv')))
    >>> f = Friend(name='Charlie', date_of_birth=datetime.date(1988, 4, 16))
    >>> friends.append(f)
    >>> writer = Friend.writer(open('friends.csv', 'w'))
    >>> for f in friends:
    ...     writer.writerow(f)
    ... 
