from fastapi import FastAPI, Request, APIRouter
import psycopg2
from psycopg2.extras import Json

app = APIRouter()

# 连接到pgsql数据库
conn = psycopg2.connect(database='postgres', user='postgres',password='aKtALRFAKCRC', host='81.68.157.7', port=5432)
cur = conn.cursor()

# 定义一个API路由，用于接收前端发送的POST请求，并将请求体中的数据插入到数据库中
@app.post("/pesticide/")
async def add_pesticide(request: Request):
    # 获取请求体中的json数据
    data = await request.json()
    # 判断表 pesticide 是否存在
    cur.execute("select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE' and table_name='pesticide'")
    count = cur.fetchone()[0]

    # 如果表不存在，则新建表
    if count == 0:
        cur.execute("create table pesticide (data json)")
        conn.commit()

    # 执行插入操作
    cur.execute("insert into pesticide (data) values (%s)", [Json(data)])
    conn.commit()
    return {"message": "Pesticide added successfully"}

@app.get("/pesticide/{name}")
def get_pesticide(name: str):
    # 查询数据库中匹配的数据
    cur.execute("SELECT data FROM pesticide WHERE data->>'name' = %s", (name,))
    result = cur.fetchone()
    # 如果有结果，返回json格式的响应，否则返回错误信息
    if result:
        return result["data"]
    else:
        return {"error": "No such pesticide"}