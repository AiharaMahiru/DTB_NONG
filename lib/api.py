from fastapi import FastAPI, Request, APIRouter
import psycopg2
from lib.pgsql import connect_db, read_json, creat_table, into_data

app = APIRouter()

# 连接到pgsql数据库
conn, cur = connect_db()

# 定义一个API路由，用于接收前端发送的POST请求，并将请求体中的数据插入到数据库中
@app.post("/pesticide/")
async def add_pesticide(request: Request):
    # 获取请求体中的json数据
    data = await request.json()
    # 将数据插入到数据库中
    creat_table()
    into_data(data)
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