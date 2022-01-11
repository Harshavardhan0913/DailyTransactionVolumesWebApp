import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS balanceHistory(token TEXT,balance NUMBER , insertedOn TIMESTAMP )")
        self.conn.commit()

    def getBalances(self):
        self.cursor.execute("SELECT * FROM balanceHistory ORDER BY insertedOn desc LIMIT 10 ")
        data = self.cursor.fetchall()
        return data

    def addBalanceHistory(self, data):
        #self.cursor.execute(f"DELETE FROM balanceHistory")

        sql_statement = "INSERT INTO balanceHistory (token, balance, insertedOn) VALUES (?,?,?)"
        self.cursor.executemany(sql_statement, data)
        self.conn.commit()

