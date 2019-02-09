import MySQLdb
class ToDB():
    def __init__(self):
        self.db = MySQLdb.connect('localhost', 'root', '12345', "jp", 3306, charset='utf8mb4')
        self.cursor = self.db.cursor()
    def search(self, sql):
        cur = self.cursor
         # 这一条语句是告诉数据库编码方式为 utf8
        cur.execute("set names utf8mb4 ")
        cur.execute(sql)
        results = cur.fetchone()
        if not results:
            return None
        return {
            'name':results[0],
            'price':results[1]
        }
    def runSql(self,sql):
        cur = self.cursor
        cur.execute("set names utf8mb4 ")
        cur.execute(sql)
        self.db.commit()
    def searchCode(self, sql):
        cur = self.cursor
         # 这一条语句是告诉数据库编码方式为 utf8
        cur.execute("set names utf8mb4 ")
        cur.execute(sql)
        results = cur.fetchone()

        if not results:
            return None
        return results
    def insertMany(self,sql,data):
        cursor = self.cursor
        try:
            cursor.executemany(sql, data)
        except Exception as e:
            print(e)
            self.db.rollback()
        self.db.commit()


if __name__=="__main__":
    db=ToDB()
    sql = "select 名称,售价 from 库存 where 条码='{0}'".format('D9787557602765')
    db.search(sql)