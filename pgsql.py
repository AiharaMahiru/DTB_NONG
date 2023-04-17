import json
import psycopg2
from psycopg2.extras import Json

# 将json数据转换成python字典
json_data = {
    "敌敌畏":{
        "name":"敌敌畏",
        "type":"杀虫剂",
        "price":10,
        "count":100,
        "inventory":100,
        "info":{
            "用途":"杀虫",
            "用量":"1ml/平方米",
            "有效期":"1年"
        }
    }
}

# 连接到pgsql数据库
conn = psycopg2.connect(database="testdb", user="postgres", password="123456", host="127.0.0.1", port="5432")
cur = conn.cursor()

# 创建一个表，如果不存在的话
cur.execute("CREATE TABLE IF NOT EXISTS pesticide (id serial PRIMARY KEY, data jsonb);")

# 将字典数据插入到表中
cur.execute("INSERT INTO pesticide (data) VALUES (%s)", [Json(json_data)])

# 插入一条新的数据到 “public”.“scene” 表中
# cur.execute('INSERT INTO "public"."scene" VALUES (%s, %s)', ('09', '智能农业'))

# 更新
# cur.execute('UPDATE "public"."scene" SET name = %s WHERE scene_id = %s;', ('5G智慧农业', '09'))

# 删除
# cur.execute('DELETE FROM "public"."scene" WHERE id = \'09\';')

# 查询
# cur.execute('SELECT * FROM "public"."scene" WHERE name LIKE \'智慧农业\';')


# 执行查询语句
# cur.execute('SELECT * FROM "public"."scene"')

# 获取所有结果
# rows = cur.fetchall()

# 打印结果
# for row in rows:
#     print(row)

# 提交并关闭连接
conn.commit()
cur.close()
conn.close()