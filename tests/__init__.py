import unittest, os, shutil
import logging
import getpass

from pylocated import locatedb, PyLocatedException

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


class TestLocate(unittest.TestCase):


    def test_version(self):
        version = locatedb.version()
        log.info(version)
        self.assertIsNotNone(version)

    def test_find(self):
        buffer = locatedb.find('__init__.py', ignore_case=False, limit=2)
        str_list = buffer.getvalue().split("\n")
        log.info(str_list)
        self.assertEqual(len(str_list), 2)

    def test_find_regex(self):
        buffer = locatedb.find('__init__.py', ignore_case=False, limit=2, regex='/home/plasmashadow/.PyCharm40/system/python_stubs/-1235803962/Crypto/Cipher/*')
        str_list = buffer.getvalue().split("\n")
        log.info(str_list)
        self.assertEqual(len(str_list), 1)

    def test_statistics(self):
        file_obj = locatedb.statistics()
        log.info(file_obj.__dict__)
        self.assertIsNotNone(file_obj.directories)
        self.assertIsNotNone(file_obj.files)
        self.assertIsNotNone(file_obj.totalspace)
        self.assertIsNotNone(file_obj.usedspace)

    def test_instance_find(self):
        locate_obj = locatedb()
        buffer = locate_obj.find('__init__.py', ignore_case=False, limit=2)
        str_list = buffer.getvalue().split("\n")
        log.info(str_list)
        self.assertEqual(len(str_list), 2)

    def test_instance_count(self):
        locate_obj = locatedb()
        buffer = locate_obj.count('__init__.py')
        log.info(buffer)
        self.assertIsNotNone(buffer)

class TestLocateWithKwArgs(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLocateWithKwArgs, self).__init__(*args, **kwargs)
        self.test_file = '/tmp/db123.db'

    def setUp(self):
        if os.path.isfile(self.test_file):
            os.unlink(self.test_file)
        elif os.path.isdir(self.test_file):
            shutil.rmtree(self.test_file)
        else:
            pass

    def tearDown(self):
        if os.path.isfile(self.test_file):
            os.unlink(self.test_file)

    def create_obj(self):
        locate_obj = locatedb(db_path=self.test_file)

    def test_instance_with_dbpath(self):
        if getpass.getuser() == 'root':
            self.create_obj()
            self.assertEqual(os.path.isfile(self.test_file), True, "instance triggered updatedb")
        else:
            self.assertRaises(PyLocatedException, self.create_obj)
