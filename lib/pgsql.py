import json
import psycopg2
# from psycopg2.extras import Json

def connect_db():
    # 连接数据
    conn = psycopg2.connect(database='postgres', user='postgres',
                            password='aKtALRFAKCRC', host='81.68.157.7', port=5432)
    cur = conn.cursor()
    return cur, conn


# 读取json文件
def read_json():
    json_data = open('src/nong.json', 'r', encoding='utf-8')
    data = json_data.read()
    data = json.loads(data)
    return data

def creat_table():
    cur.execute("""
    SELECT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_name = 'pesticide'
    )
    """)
    # 判断表是否存在
    table_exists = cur.fetchone()[0]

    if not table_exists:

        cur.execute("""
                CREATE TABLE pesticide (
                    name VARCHAR(255) PRIMARY KEY,
                    type VARCHAR(255),
                    unit_price INTEGER,
                    purchase_quantity INTEGER,
                    stock INTEGER,
                    purpose VARCHAR(255),
                    dosage VARCHAR(255),
                    expiration_date VARCHAR(255)
                )
            """)
        conn.commit()

def into_data(data):
    # 遍历json键值对
    for pesticide_name, pesticide_data in data.items():
        cur.execute(
            "INSERT INTO pesticide (name, type, unit_price, purchase_quantity, stock, purpose, dosage, expiration_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                pesticide_data["名称"],
                pesticide_data["类型"],
                pesticide_data["单价"],
                pesticide_data["购买数量"],
                pesticide_data["库存"],
                pesticide_data["用途"],
                pesticide_data["用量"],
                pesticide_data["有效期"]
            )
        )

        conn.commit()

# 创建一个表，如果不存在的话
# cur.execute("CREATE TABLE IF NOT EXISTS pesticide (id serial PRIMARY KEY, data jsonb);")

# 将字典数据插入到表中
# cur.execute("INSERT INTO pesticide (data) VALUES (%s)", [Json(json_data)])

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