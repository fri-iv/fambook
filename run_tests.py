import unittest
from apps.users.tests import AuthTestCase
# from apps.notes.tests import NotesTestCase
from libs.router import load_routs


if __name__ == '__main__':
    load_routs()
    unittest.main()
