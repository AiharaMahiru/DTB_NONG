from fastapi import Request, APIRouter
from lib.pgsql import connect_db, creat_table, into_data, read_table

app = APIRouter()

# 连接到pgsql数据库
# conn, cur = connect_db()

# 定义一个API路由，用于接收前端发送的POST请求，并将请求体中的数据插入到数据库中
@app.post("/pesticide/add?")
async def add_pesticide(request: Request):
    # 获取请求体中的json数据
    data = await request.json()
    if not data:
        return {"message": "Pesticide added failed"}
    else:
    # 将数据插入到数据库中
        creat_table()
        into_data(data)
    return {"message": "Pesticide added successfully"}


# 读取整个pesticide表
@app.get("/pesticide/table")
async def read_pesticide():
    rows = await read_table()
    return {"data": rows , "message": "Pesticide read successfully"}
