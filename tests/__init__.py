import unittest

from pylocated import locatedb
import logging
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
