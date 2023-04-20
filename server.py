import psycopg2
# from psycopg2.extras import Json
import json

# 读取json文件
def read_json():
    json_data = open('src/nong.json', 'r', encoding='utf-8')
    data = json_data.read()
    data = json.loads(data)
    return data

# 传参给data
data = read_json()

# 连接数据
conn = psycopg2.connect(database='postgres', user='postgres',
                        password='aKtALRFAKCRC', host='81.68.157.7', port=5432)
cur = conn.cursor()

# 创建表
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

# conn.commit()
cur.close()
conn.close()
