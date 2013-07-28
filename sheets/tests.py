import unittest
times2 = lambda value: value * 2

class MultiplicationTests(unittest.TestCase):

    def setUp(self):
        self.factor = 2

    def testNumber(self):
        self.assertEqual(times2(5), 42)

    def testString(self):
        self.assertTrue(times2(5) == 10)

    def testTuple(self):
        self.assertTrue(times2(5) == 10)


if __name__ == '__main__':
    unittest.main()


