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

# 提交并关闭连接
conn.commit()
cur.close()
conn.close()