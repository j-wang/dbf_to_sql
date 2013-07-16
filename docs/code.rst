Module Documentation
======================

:mod: `dbf_to_sql` - Converts FoxPro Tables to SQL
=====================================================

.. module:: dbf_to_sql
   :synopsis: Processes FoxPro Tables into SQL Tables.
.. moduleauthor:: James Wang <james@j-wang.net>

This module essentially glues together dbfpy and sqlalchemy to convert FoxPro tables into SQL tables (specifically, sqlite -- although this should be easy to adapt and might work out of the box for dialects that sqlalchemy supports, it has not been tested for those cases).

Requires dbf and sqlalchemy (both of which are available through pip install)

.. class:: Converter(sqldb[, sql='sqlite'])

  Converts a FoxPro database (directory of .dbf files) to an sqlite3 database stored on disk (will overwrite if already exists).

  Theoretically can work for any sql dialect that sqlalchemy supports, but in reality has just been tested for sqlite (and is expected to break in subtle to not-so-subtle ways for other dialects). Use for other dialects at your own risk.

  Example::

    fp2sql = Converter('sqldata.db')
    fp2sql.convert_dbfs('foxpro_app/data/')

  Alternatively::

    fp2.sql.convert_dbf('clients.dbf')

Methods
=========

.. method:: convert_dbf(foxpro_source)

   Reads .dbf file and converts to specified sql database, preserving the schema of the foxpro database (as best it can).

.. method:: convert_dbfs(foxpro_dir)

   Reads FoxPro database (given as a directory containing .dbf files).

.. classmethod:: convert_type(typ_tuple)

   Takes a field_info tuple (called from dbf.Table.field_info) and converts dbfpy type information into sqlalchemy type information.

.. classmethod:: fix_record(read_string, col_type)

   Takes record data as a read_string from dbf and an sqlalchemy datatype (e.g. sqlalchemy.Integer). Performs simple typecasting depending on type, and tries to handle bytestrings.

   Needless to say, this won't save you from corrupted/badly mangled data.

