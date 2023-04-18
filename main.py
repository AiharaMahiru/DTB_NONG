from lib.until import *
# Path: lib/until.py

obj = {
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
    },
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

# 将字典数据插入到表中
# cur.execute("INSERT INTO pesticide (data) VALUES (%s)", [Json(obj)])

print(to_table_json(obj, 1, 2))
