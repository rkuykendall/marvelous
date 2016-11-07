import unittest

import marvelous
from marvelous.exceptions import AuthenticationError


class TestInit(unittest.TestCase):
    def setUp(self):
        pass

    def test_api(self):
        with self.assertRaises(AuthenticationError):
            marvelous.api()

        with self.assertRaises(AuthenticationError):
            marvelous.api(private_key="Something")

        with self.assertRaises(AuthenticationError):
            marvelous.api(public_key="Something")

        m = None
        try:
            m = marvelous.api(public_key="Something", private_key="Else")
        except Exception as exc:
            self.fail("marvelous.api() raised {} unexpectedly!".format(exc))

        self.assertEquals(
            m.__class__.__name__, marvelous.session.Session.__name__)

if __name__ == '__main__':
    unittest.main()
