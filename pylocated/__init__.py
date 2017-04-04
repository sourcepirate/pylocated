from subprocess import Popen, check_output, call
from subprocess import PIPE as pipe
import re, traceback, os, getpass, six, sys

# import StringIO according to Python version


if six.PY2:
    from cStringIO import StringIO
else:
    if sys.version_info.minor <= 3:
        from StringIO import StringIO
    else:
        from io import StringIO


class PyLocatedException(Exception):
    """
    Base Exception for all pylocated
    error
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return '<%s>%s' % (self.__class__.__name__, self.message)

    def __repr__(self):
        return str(self)


class BiContextual(object):
    """
       Used to get the values of class from meta object type and
       object name from instance method
    """

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, type=None):
        if instance is None:
            return getattr(type, '_class_' + self.name)
        return getattr(instance, '_instance_' + self.name)

class FileSystem(object):
    def __init__(self, statics_string):
        self.string = statics_string
        self.parsed = statics_string.split("\n\t")

    @property
    def directories(self):
        dir_str = self.parsed[1].strip().split()
        _directories = dir_str[0].replace(",", "")
        return long(_directories)

    @property
    def files(self):
        file_str = self.parsed[2].strip().split()
        _files = file_str[0].replace(",", "")
        return long(_files)

    @property
    def totalspace(self):
        total_str = self.parsed[3].strip().split()
        _total_str = total_str[0].replace(",", "")
        return long(_total_str)

    @property
    def usedspace(self):
        total_str = self.parsed[4].strip().split()
        _total_str = total_str[0].replace(",", "")
        return long(_total_str)

    @property
    def db_path(self):
        return self.parsed[0].split()[1]


def _docommand(args):
    try:
        stream = Popen(args, stdout=pipe, stderr=pipe)
        out, err = stream.communicate()
        if err:
            raise PyLocatedException(err)
        return out
    except Exception as e:
        print(traceback.format_exc(e))
        raise PyLocatedException(str(e))


class locatedb(object):

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
            raise PyLocatedException("Root user privilege is required to perform updatedb")

        args = ['updatedb']
        if db_path:
            args.extend(['-o', db_path])

        try:
            stream = Popen(args, stdout=pipe, stderr=pipe)
            out, err = stream.communicate()
            if err:
                raise PyLocatedException(err)
            return out
        except Exception as e:
            raise PyLocatedException(str(e))

    @classmethod
    def _class_count(cls, name, ignore_case=False):
        args = ['locate', '-c', name]
        if ignore_case:
            args.extend(['-i'])
        return _docommand(args)

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
        if limit and isinstance(limit, (int, long)):
            args.extend(['-l', str(limit)])
        process_pipe = _docommand(args)
        process_pipe = process_pipe.split("\n")
        if regex:
            try:
                compiled = re.compile(regex)
            except Exception as e:
                raise PyLocatedException("Invalid regular expression")
            process_pipe = filter(lambda x: compiled.match(x), process_pipe)

        out_put = filter(lambda x: x is not '', process_pipe)

        buffer = StringIO()
        buffer.writelines("\n".join(out_put))
        return buffer

    def _instance_find(self, name, ignore_case=False, limit=None, regex=None):

        args = ['locate', name]
        if ignore_case:
            args.extend(['-i'])
        if limit and isinstance(limit, (int, long)):
            args.extend(['-l', str(limit)])
        if self.db_path:
            args.extend(['-d', self.db_path])

        process_pipe = _docommand(args)
        process_pipe = process_pipe.split("\n")

        if regex:
            try:
                compiled = re.compile(regex)
            except Exception as e:
                raise PyLocatedException("Invalid regular expression")
            process_pipe = filter(lambda x: compiled.match(x), process_pipe)

        out_put = filter(lambda x: x is not '', process_pipe)

        buffer = StringIO()
        buffer.writelines("\n".join(out_put))
        return buffer

    find = BiContextual("find")

    @classmethod
    def _class_statistics(cls):
        args = ['locate', '-S']
        out = _docommand(args)
        return FileSystem(out)

    def _instance_statistics(self):
        args = ['locate', '-S']
        if self.db_path:
            args.extend(['-d', self.db_path])
        return _docommand(args)

    statistics = BiContextual("statistics")

    @classmethod
    def version(cls):
        args = ['locate', '-V']
        out = _docommand(args)
        version = out.split("\n")[0].split()[1]
        return version

# Expose updatedb function
updatedb = locatedb.updatedb
