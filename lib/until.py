import json

convert_funcs = {
    'str': str,
    'li': list,
    'dic': dict,
    'json_loads': json.loads,
    'json_dumps': json.dumps,
    'float': float
}

# 在get_without_none函数中，用get方法来获取转换函数并调用它
def get_without_none(s, ret_type=None):
    try:
        # 如果ret_type在字典中存在，就获取对应的转换函数，否则就返回None
        convert_func = convert_funcs.get(ret_type)
        # 如果convert_func不为None，就调用它，否则就返回s
        ret = convert_func(s) if convert_func else s
    except:
        if ret_type == 'float':
            ret = 0
        else:
            ret = ''
    return ret

# 使用None作为返回值
def data_judge(s, judge_type=None):
    try:
        ret = None
        if judge_type == 'float':
            ret = float(s)
        elif judge_type == 'int':
            ret = int(s)
    except:
        return None
    return ret

# 指定具体的异常类型或者处理方式
def get_limit_offset(page=None, limit=None):
    try:
        page = int(page)
        limit = int(limit)
        offset = (page - 1) * limit
    except ValueError:
        # 可以打印错误信息或者抛出异常
        print('Invalid page or limit')
        raise ValueError('Invalid page or limit')
        # 或者给limit和offset赋默认值
        limit = None
        offset = 0
    return limit, offset

# 使用参数化查询的方式来生成sql语句
def get_sql(sql, sql_content=None):
    # 定义一个字典，键为sql_content，值为对应的sql语句
    sql_dict = {
        "count": "select count(1) from ({}) as sql_data",
        "detail": "{} limit :limit offset :offset",
        None: "{}"
    }
    # 用format方法来插入sql参数，用get方法来获取对应的sql语句
    return sql_dict.get(sql_content).format(sql) + ';'

# 直接使用对象的__dict__属性来返回一个字典
def convert_to_builtin_type(obj):
    return obj.__dict__

def to_table_json(obj, page, limit):
    pageObj = obj[(page - 1) * limit:page * limit]
    j = json.dumps(pageObj, default=convert_to_builtin_type)
    return json.dumps({
        "code": 0,
        "count": len(obj),
        "data": j
    })

def to_all_table_json(obj):
    j = json.dumps(obj, default=convert_to_builtin_type)
    return json.dumps({
        "code": 0,
        "count": len(obj),
        "data": j
    })