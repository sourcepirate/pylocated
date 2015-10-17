##PyLocated

A Locatedb interface for python

##Installing

```
  pip install pylocated

```

##Usage

```python
from pylocated import locatedb

#if you want to use default locatedb path you
#can use the class methods for it.

buffer = locatedb.find('sample.py', limit=20, ignore_case=False, regex=None)
files = buffer.getvalue()
print files

#if you want to setup you own path to locatedb

locate_db = locatedb(db_path='/var/bin/hello')
buffers = locate_db.find("sample.py", limit=20, ignore_case=False, regex=None)
print buffers.getvalue()

```

##API

###locatedb.find or instance.find(): [name, limit=None, ignore_case=False, regex=None]
   used to find the particular files in system.
   where pattern inside regex find the matches of path.
   
###locatedb.count or instance.count: [name]
   used find the number of occurences for that particular word.
   equivalent to locate -c

###locatedb.statistics or instance.statistics : [name]
   used to give the disk statistics
   equivalent to locate -S
   
###locatedb.version: 
   return the version of locatedb you are using.
   
   
##License:
  <b>MIT</b>
  &copy; 2015 plasmashadow  
  plasmashadowx@gmail.com
