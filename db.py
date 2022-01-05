import sqlite3
from sqlite3 import Error

class database():
    def sql_connection(self):
        try:
            con = sqlite3.connect('mydatabase.db')
            # print("connection established")
            return con
        except Error:
            print(Error)

    def create_sql_table(self, con):
        cursor = con.cursor()
        cursor.execute("CREATE TABLE releases(ROWID integer PRIMARY KEY, iOS int, macOS int, tvOS int, watchOS int)")
        con.commit()

    def sql_insert(self, con, insert_lst):
        cursor = con.cursor()  
        values = tuple()
        for item in insert_lst:
            values += (item, )  
        cursor.execute('INSERT INTO releases(iOS, macOS, tvOS, watchOS) VALUES(?, ?, ?, ?)', values)    
        con.commit()

    def sql_select(self, con):
        cursor = con.cursor()    
        cursor.execute('SELECT * FROM releases ORDER BY ROWID desc LIMIT 1')  
        rows = cursor.fetchall()  
        return rows

    def sql_create_table_if_not_exists(self, con):
        cursor = con.cursor()
        cursor.execute('create table if not exists releases(ROWID integer PRIMARY KEY, iOS int, macOS int, tvOS int, watchOS int)')
        con.commit()

    def drop_table(self, con):
        cursor = con.cursor()
        cursor.execute('DROP table if exists releases')
        con.commit()

# con = sqlite3.conect('mydatabase.db')

