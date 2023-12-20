import sqlite3


class Base:
    def __init__(self):
        self.bd = sqlite3.connect('RPG.sqlite')

    def get_all_information(self, object, table, condition='True'):
        result = self.bd.execute(f"""SELECT {object} FROM {table}
           WHERE {condition}""").fetchall()
        return result

    def close(self):
        self.bd.close()
