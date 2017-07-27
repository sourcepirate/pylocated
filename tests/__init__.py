import unittest
import os
import logging
from pylocated import locatedb

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(ROOT, 'locatedir')


class TestLocate(unittest.TestCase):
    def setUp(self):
        locatedb.updatedb(db_path='/tmp/fixed.db', path=PATH)

    def tearDown(self):
        import os
        os.unlink('/tmp/fixed.db')

    def test_version(self):
        version = locatedb.version()
        self.assertIsNotNone(version)
        self.assertTrue(float(version))

    def _assert_is_in(self, what, where):
        path = where.getvalue().split("\n")
        self.assertTrue(len(path) == 1)
        path = path[0]
        expected = os.path.join(PATH, what)
        self.assertEqual(path, expected)

    def test_find(self):
        self._assert_is_in('foobar', locatedb(db_path='/tmp/fixed.db').find(
            'foobar', ignore_case=False, limit=2))

    def test_find_regex(self):
        self._assert_is_in(
            'barstuff.py',
            locatedb.find('py', ignore_case=False, regex=r'.*.py$',
                          db_path='/tmp/fixed.db'))

    def test_statistics(self):
        file_obj = locatedb.statistics(db_path='/tmp/fixed.db')
        log.info(file_obj.__dict__)
        self.assertEqual(file_obj.directories, 1)
        self.assertEqual(file_obj.files, 3)
        self.assertTrue(float(file_obj.totalspace) > 100)
        self.assertTrue(float(file_obj.usedspace) > 100)

    def test_instance_find(self):
        self._assert_is_in(
            'foobar',
            locatedb(db_path="/tmp/fixed.db").find('foobar'))

    def test_instance_count(self):
        self.assertEqual(locatedb(db_path='/tmp/fixed.db').count('foobar'), 1)

    def test_instance_update(self):
        locatedb.updatedb(db_path='/tmp/testdb', path=PATH)
        self.assertTrue(os.path.isfile('/tmp/testdb'))
