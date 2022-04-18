import sqlite3

class SqlTable:
    def __init__(self, manager, fieldslist: list):
        self.man = manager
        self.fields = fieldslist
        fields = '('
        for i in fieldslist[:-1]:
            fields += i + ','
        fields += fieldslist[-1] + ')'
        manager.exec("CREATE TABLE IF NOT EXISTS %s %s" % (self.__class__.__name__, fields))

    def insert(self, *args):
        if len(args) != len(self.fields):
            print(self.fields)
            print(args)
            raise Exception('Wrong number of arguments!')
        values = '('
        for i in args[:-1]:
            values += '"' + str(i) + '",'
        values += '"' + str(args[-1]) + '")'
        self.man.exec("INSERT INTO %s VALUES %s" % (self.__class__.__name__, values))

    def listall(self):
        self.man.cursor.execute("SELECT * FROM %s" % self.__class__.__name__)
        return self.man.cursor.fetchall()

    def listfiltered(self, where):
        self.man.cursor.execute("SELECT * FROM %s WHERE %s" % (self.__class__.__name__, where))
        return self.man.cursor.fetchall()

class SqlManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def exec(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()