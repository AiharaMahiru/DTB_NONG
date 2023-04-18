import json


# None数据处理
def get_without_none(s, ret_type=None):
    try:
        if ret_type == 'str':
            ret = '' if s is None else str(s)
        elif ret_type == 'li':
            ret = [] if s is None else list(s)
        elif ret_type == 'dic':
            ret = {} if s is None else dict(s)
        elif ret_type == 'json_loads':
            ret = '' if s is None else json.loads(s)
        elif ret_type == 'json_dumps':
            ret = '' if s is None else json.dumps(s)
        elif ret_type == 'float':
            ret = 0 if s is None else float(s)
        else:
            ret = '' if s is None else s
    except:
        if ret_type == 'float':
            ret = 0
        else:
            ret = ''
    return ret


# 数据转换
def data_judge(s, judge_type=None):
    try:
        ret = ''
        if judge_type == 'float':
            ret = float(s)
        elif judge_type == 'int':
            ret = int(s)
    except:
        return False
    return ret


# 格式化 分页 字段
def get_limit_offset(page=None, limit=None):
    try:
        page = int(page)
        limit = int(limit)
        offset = (page - 1) * limit
    except:
        limit = None
        offset = 0
    return limit, offset


# 生成sql语句 根据条件
def get_sql(sql, sql_content=None):
    if sql_content == "count":
        sql = """
        select count(1) from (
        """ + sql + " ) as sql_data;"
    elif sql_content == "detail":
        sql += f" limit :limit offset :offset;"
    else:
        sql += ';'

    return sql


# json化所需的函数
def convert_to_builtin_type(obj):
    dic = {
    }
    dic.update(obj.__dict__)
    return dic


# 实例json化
def to_json(obj):
    return json.dumps(obj, default=convert_to_builtin_type)


# 分页json化并转换成表格所需
def to_table_json(obj, page, limit):
    pageObj = obj[(page - 1) * limit:page * limit]
    j = json.dumps(pageObj, default=convert_to_builtin_type)
    return """
        {
          "code": 0,
          "count": """ + str(len(obj)) + """,
          "data": """ + j + """
        } 
        """


# 全部json化并转换成表格所需
def to_all_table_json(obj):
    j = json.dumps(obj, default=convert_to_builtin_type)
    return """
        {
          "code": 0,
          "count": """ + str(len(obj)) + """,
          "data": """ + j + """
        } 
        """
