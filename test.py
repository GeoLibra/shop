import MySQLdb
def GetInfo(db, data):
    data = data.strip()
    print(data)
    ret = 0.0
    try:
        cur = db.cursor()
        sql = "set names utf8mb4 "  # 这一条语句是告诉数据库编码方式为 utf8
        cur.execute(sql)

        sql = "select * from 库存 where 条码='{0}'".format(data)
        # print sql
        cur.execute(sql)
        # sql = "select * from productinfo where(code=%s)"
        # cur.execute(sql,data)
        results = cur.fetchall()
        if len(results)==0:
            print("未找到该药品!")
            return
        # print results
        for row in results:
            # 条码
            code = row[0]
            # print code
            # 名称
            name = row[1]
            # 成本
            cost = row[2]
            # 售价
            sale =  row[3]
            print('名称:', name,  '售价:', sale)
            return {
                '名称':name,
                '售价':sale
            }

    except Exception as e:
        print(e)
db = MySQLdb.connect('localhost', 'root', '12345', "jp", 3306, charset = 'utf8mb4')
cursor = db.cursor()
sum = 0.0
while True:
    data = input("扫描输入药品条形码:")
    if data:
        # print data
        sum += GetInfo(db, data)['sale']
        print('总付款:', sum)

db.close()
