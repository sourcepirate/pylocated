""" Python locate interface library """

from subprocess import PIPE as pipe
from subprocess import Popen
import getpass
import os
import re
import sys

# import StringIO according to Python version
# Also, workaround long type

PY2 = sys.version_info[0] == 2

if PY2:
    from cStringIO import StringIO
else:
    if sys.version_info.minor <= 3:
        from StringIO import StringIO
    else:
        from io import StringIO


def _isnumeric(what):
    if not PY2:
        return str(what).isnumeric()
    else:
        try:
            float(what)
            return True
        except:
            return False


class PyLocatedException(Exception):
    """
    Base Exception for all pylocated
    error
    """
    pass


class BiContextual(object):
    """ Used to get the values of class from meta object type and
        object name from instance method
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, type_=None):
        if instance is None:
            return getattr(type_, '_class_' + self.name)
        return getattr(instance, '_instance_' + self.name)


class FileSystem(object):
    """ Filesystem object, returns statistics """
    def __init__(self, statics_string):
        self.string = statics_string
        self.parsed = statics_string.split("\n\t")

    @property
    def directories(self):
        """ Return directories found """
        return float(self.parsed[1].strip().split()[0])

    @property
    def files(self):
        """ Return files found """
        return float(self.parsed[2].strip().split()[0])

    @property
    def totalspace(self):
        """ Return total space """
        return float(self.parsed[3].strip().split()[0])

    @property
    def usedspace(self):
        """ Return used space """
        return float(self.parsed[4].strip().split()[0])

    @property
    def db_path(self):
        """ Return current locate db path """
        return self.parsed[0].split()[-1][:-1]


def _docommand(args):
    try:
        stream = Popen(args, stdout=pipe, stderr=pipe, env={'LC_ALL': 'C'})
        out, err = stream.communicate()
        if err:
            raise PyLocatedException(err)
        if not PY2:
            return out.decode()
        return out
    except Exception as err:
        # TODO: Eating up real exceptions type is questionable...
        raise PyLocatedException(str(err))


# pylint: disable=invalid-name
class locatedb(object):
    """ Locatedb """

    def __init__(self, db_path=None):
        self.db_path = db_path
        # Invoke updatedb if a custom db_path is given and which is not exist
        if db_path is not None and os.path.isfile(db_path) is False:
            self.__class__.updatedb(db_path=self.db_path)

    @classmethod
    def updatedb(cls, db_path=None):
        """
          Used to update the located db
          Equivalent to `updatedb`
        """
        if getpass.getuser() != 'root':
            raise PyLocatedException(
                "Root user privilege is required to perform updatedb")

        args = ['updatedb']
        if db_path:
            args.extend(['-o', db_path])

        try:
            stream = Popen(args, stdout=pipe, stderr=pipe)
            out, err = stream.communicate()
            if err:
                raise PyLocatedException(err)
            return out
        except Exception as err:
            raise PyLocatedException(str(err))

    @staticmethod
    def _get_buffer_from_pipe(process_pipe, regex):
        process_pipe = (a for a in process_pipe.split("\n") if a)
        if regex:
            try:
                compiled = re.compile(regex)
            except Exception:
                raise PyLocatedException("Invalid regular expression")
            process_pipe = (a for a in process_pipe if compiled.match(a) and a)
        buffer_ = StringIO()
        buffer_.writelines("\n".join(process_pipe))
        return buffer_

    @classmethod
    def _class_count(cls, name, ignore_case=False, db_path=None):
        args = ['locate', '-c', name]
        if ignore_case:
            args.extend(['-i'])
        if db_path:
            args.extend(['-d', db_path])
        return float(_docommand(args))

    def _instance_count(self, name, ignore_case=False):
        args = ['locate', '-c', name]
        if ignore_case:
            args.extend(['-i'])
        if self.db_path:
            args.extend(['-d', self.db_path])
        return _docommand(args)

    count = BiContextual("count")

    @classmethod
    def _class_find(cls, name, ignore_case=False, limit=None, regex=None):

        args = ['locate', name]
        if ignore_case:
            args.extend(['-i'])
        if limit and str(limit).isnumeric():
            args.extend(['-l', str(limit)])

        process_pipe = _docommand(args)
        return cls._get_buffer_from_pipe(process_pipe, regex)

    def _instance_find(self, name, ignore_case=False, limit=None, regex=None):
        args = ['locate', name]

        if ignore_case:
            args.extend(['-i'])
        if limit and str(limit).isnumeric():
            args.extend(['-l', str(limit)])
        if self.db_path:
            args.extend(['-d', self.db_path])

        process_pipe = _docommand(args)
        return self._get_buffer_from_pipe(process_pipe, regex)

    find = BiContextual("find")

    @classmethod
    def _class_statistics(cls, db_path=None):
        args = ['locate', '-S']
        if db_path:
            args.extend(['-d', db_path])
        return FileSystem(_docommand(args))

    def _instance_statistics(self):
        args = ['locate', '-S']
        if self.db_path:
            args.extend(['-d', self.db_path])
        return _docommand(args)

    statistics = BiContextual("statistics")

    @classmethod
    def version(cls):
        """ Return locate version """
        return _docommand(['locate', '-V']).split("\n")[0].split()[1]


# Expose updatedb function
# pylint: disable=invalid-name
updatedb = locatedb.updatedb
