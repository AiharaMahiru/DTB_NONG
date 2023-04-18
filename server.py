import psycopg2
from psycopg2.extras import Json

conn = psycopg2.connect(database='postgres', user='postgres',
                        password='aKtALRFAKCRC', host='81.68.157.7', port=5432)
cur = conn.cursor()
# 判断表 pesticide 是否存在
cur.execute("select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE' and table_name='pesticide'")
count = cur.fetchone()[0]
if count == 0:
    # 根据 JSON 数据的键创建列
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
    columns = ", ".join([f"{key} json" for key in json_data.keys()])
    cur.execute(f"create table pesticide ({columns})")
    conn.commit()

# 执行插入操作
placeholders = ", ".join(["%s"] * len(json_data))
values = list(json_data.values())
cur.execute(f"insert into pesticide values ({placeholders})", values)
conn.commit()
cur.close()
conn.close()