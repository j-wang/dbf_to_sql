"""
:mod: `dbf_to_sql` - Converts FoxPro Tables to SQL
============================

.. module:: dbf_to_sql
   :synopsis: Processes FoxPro Tables into SQL Tables.
   :original_date: 15 Jul 2013
.. moduleauthor:: James Wang <james@j-wang.net>

This module essentially glues together dbfpy and sqlalchemy to convert FoxPro
tables into SQL tables (specifically, sqlite -- although this should be easy to
adapt and might work out of the box for dialects that sqlalchemy supports, it
has not been tested for those cases).

Requires dbf and sqlalchemy (both of which are available through pip install)

"""
import dbf
import sqlalchemy
import os
import datetime


class Converter(object):
    """
    Converts a FoxPro database (directory of .dbf files) to an sqlite3
    database stored on disk (will overwrite if already exists).

    Theoretically can work for any sql dialect that sqlalchemy supports, but in
    reality has just been tested for sqlite (and is expected to break in subtle
    to not-so-subtle ways for other dialects). Use for other dialects at your
    own risk.

    Example:
    ::

             fp2sql = Converter('sqldata.db')
             fp2sql.convert_dbfs('foxpro_app/data/')

    Alternatively:
    ::

             fp2.sql.convert_dbf('clients.dbf')

    """
    sa_types = {'M': sqlalchemy.String,
                'N': sqlalchemy.Integer,
                'T': sqlalchemy.DateTime,
                'L': sqlalchemy.Boolean}

    def __init__(self, sqldb, sql='sqlite'):
        self.engine = sqlalchemy.create_engine('{0}:///{1}'.format(sql, sqldb),
                                               echo=True)
        self.meta = sqlalchemy.MetaData()

    def convert_dbf(self, foxpro_source):
        """
        Reads .dbf file and converts to specified sql database, preserving the
        schema of the foxpro database (as best it can).

        """
        conn = self.engine.connect()
        dbf_table = dbf.Table(foxpro_source)
        schema = dbf_table.field_names

        # translate foxpro db schema to sqlite
        cols = []
        col_types = {}
        for field in schema:
            col_type = self.convert_type(dbf_table.field_info(field))
            cols.append(sqlalchemy.Column(field, col_type))
            col_types[field] = col_type

        # split out dir, take filename, truncate .dbf
        table_name = foxpro_source.split('/')[-1][:-4]

        sql_table = sqlalchemy.Table(table_name, self.meta, *cols)
        self.meta.create_all(self.engine)
        dbf_table.open()

        # deposit records into sqlite database
        for record in dbf_table:
            rec_data = {col: self.fix_record(record[col], col_types[col])
                        for col in schema}
            conn.execute(sql_table.insert().values(**rec_data))

        dbf_table.close()

    def convert_dbfs(self, foxpro_dir):
        """
        Reads FoxPro database (given as a directory containing .dbf files).

        """
        dir_contents = [f.upper() for f in os.listdir(foxpro_dir)]
        dbf_files = filter(lambda x: x.find('.DBF') != -1, dir_contents)

        for dfile in dbf_files:
            self.convert_dbf(foxpro_dir + dfile)

    @classmethod
    def convert_type(cls, typ_tuple):
        """
        Takes a field_info tuple (called from dbf.Table.field_info) and
        converts dbfpy type information into sqlalchemy type information.

        """
        typ = typ_tuple[0]
        length = typ_tuple[1]
        length2 = typ_tuple[2]

        if typ == 'N' and length2 != 0:
            return sqlalchemy.Float
        elif typ == 'C':
            return sqlalchemy.String(length)
        else:
            return cls.sa_types[typ]

    @classmethod
    def fix_record(self, string, col_type):
        """
        Takes record data as a read_string from dbf and an sqlalchemy datatype
        (e.g. sqlalchemy.Integer). Performs simple typecasting depending on
        type, and tries to handle bytestrings.

        Needless to say, this won't save you from corrupted/badly mangled data.

        """
        if col_type == sqlalchemy.Integer:
            return int(string)
        elif col_type == sqlalchemy.Boolean:
            return float(string)
        elif col_type == sqlalchemy.DateTime:
            if type(string) == datetime.datetime:
                return string
            else:
                raise TypeError("DateTime is in wrong format.")
        else:
            # Because sqlalchemy otherwise complains about bytestrings...
            # A bit dangerous, but handles case of bytestrings being used in
            # domain specific applications
            try:
                return unicode(string)
            except UnicodeDecodeError:  # bytestring (... usually)
                bytestr = str(string).encode('string_escape')
                return unicode(bytestr)


def main():
    if 'test__.db' in os.listdir('.'):
        os.remove('test__.db')
    fp2sql = Converter('test__.db')  # name-mangled for (hoped-for) safety
    fp2sql.convert_dbfs('test_data/')

if __name__ == '__main__':
    main()
