from fastapi import Request, APIRouter
from lib.pgsql import connect_db, creat_table, into_data, read_data


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

@app.get("/data/{name}}")
async def read_pesticide(name: str):
    rows = read_data(name)
    return {"data": rows}