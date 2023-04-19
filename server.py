import psycopg2
from psycopg2.extras import Json

conn = psycopg2.connect(database='postgres', user='postgres',
                        password='aKtALRFAKCRC', host='81.68.157.7', port=5432)
cur = conn.cursor()

json_data = {
    "敌敌畏": {
        "name": "敌敌畏",
        "type": "杀虫剂",
        "price": 10,
        "count": 100,
        "inventory": 100,
        "info": {
                "用途": "杀虫",
                "用量": "1ml/平方米",
                "有效期": "1年"
        }
    }
}

# 判断表 pesticide 是否存在
cur.execute("select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE' and table_name='pesticide'")
count = cur.fetchone()[0]
if count == 0:
    # 根据 JSON 数据的键创建列

    columns = ", ".join([f"{key} json" for key in json_data.keys()])
    # print(columns)
    cur.execute(f"create table pesticide ({columns})")
    conn.commit()

# 执行插入操作
placeholders: str = ", ".join(["%s"] * len(json_data))
values: list = list(json_data.values())
# [{'name': '敌敌畏', 'type': '杀虫剂', 'price': 10, 'count': 100, 'inventory': 100, 'info': {'用途': '杀虫', '用量': '1ml/平方米', '有效期': '1年'}}]

# 构造列名
columns = ", ".join(values[0].keys())

# # 构造值
values_str: str = ", ".join(["(%s)" % ", ".join(["%s"] * len(values[0]))] * len(values))

# # 构造 SQL 语句 insert into pesticide (name, type, price, count, inventory, info) values (%s, %s, %s, %s, %s, %s)
sql: str = "insert into pesticide (%s) values %s" % (columns, values_str)

# # 执行 SQL 语句
cur.execute(sql, [v for d in values for v in d.values()])
# conn.commit()
cur.close()
conn.close()
