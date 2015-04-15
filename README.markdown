# cmongo2sql
[![Build Status](https://travis-ci.org/stpettersens/cmongo2sql.svg?branch=master)](https://travis-ci.org/stpettersens/cmongo2sql) [![Build status](https://ci.appveyor.com/api/projects/status/github/stpettersens/cmongo2sql?branch=master&svg=true)](https://ci.appveyor.com/project/stpettersens/cmongo2sql)

Utility to convert a MongoDB JSON dump to a SQL dump.
For migrating data from MongoDB to MySQL or similar RDBMS.

Usage: `cmongo2sql -f data.json -o data.sql`

*Tested with Python 2.7.9 and PyPy 2.5.1 (works), IronPython 2.7.5 (use IPY tweaked version).
Does not work with Jython 2.5.3 (no json module).*
