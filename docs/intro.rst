Introduction
==============

Motivation
------------
FoxPro is a dying technology, but unfortunately, some organizations still have all of their data in it. This tool is meant to help ease transition into more modern databases (specifically sqlite3).

Synopsis
----------
This module essentially glues together dbf and SQLAlchemy to convert FoxPro tables into SQL tables (specifically, sqlite3 -- although this should be easy to adapt and might work out of the box for dialects that SQLAlchemy supports).

At this stage, I would not suggest using this for any dialect other than sqlite (which the Converter defaults to anyhow). If you need to use this with other SQL dialects, use other tools to convert the sqlite3 database to something else.

Requires `dbf <https://pypi.python.org/pypi/dbf>`_ and `SQLAlchemy <http://www.sqlalchemy.org/>`_ (both of which are open source and available through pip install).
::

    pip install dbf
    pip install sqlalchemy

Version Warning
-----------------
Testing for this module has primarily come through my own usage. Although it has been "tested," there's nothing quite like real data to muck up a theoretically sound program.

I'm not looking to use this module to do data validation or clean up horribly mangled databases, but I suspect there will be common errors (especially in domain-specific applications, which FoxPro is often used for), which I haven't yet tripped over. If you feel there's such a case, please open an issue or send me an email.

Usage
--------
You can convert directories of DBF tables directly:
::

    import dbf_to_sql
        
    fp2sql = dbf_to_sql.Converter('sqldata.db')
    fp2sql.convert_dbfs('foxpro_app/data/')

Or just individual tables:
::

    fp2.sql.convert_dbf('clients.dbf')
