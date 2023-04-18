from sqlalchemy.sql import text
from app.src.util.common import get_sql
from app.src.models.element import Scene, Element, ElementHeader, ElementParam


# 获取场景数据
def get_scene_data(db):
    sql = """select scene_id, name
              from scene 
              """

    rows = db.engine.execute(text(sql))
    data = []
    for row in rows:
        scene = Scene(scene_id=row['scene_id'], name=row['name'])
        data.append(scene)
    db.close()
    return data


# 获取元素数据
def get_element_data(db, limit=None, offset=0, id=None, scene_id=None, element_type=None, serial_number=None):
    s_id = ''
    if id is not None and id != '':
        s_id = f""" and id = :id """

    s_scene_id = ''
    if scene_id is not None and scene_id != '':
        s_scene_id = f""" and scene_id = :scene_id """

    s_element_type = ''
    if element_type is not None and element_type != '':
        s_element_type = f""" and element_type = :element_type """

    s_serial_number = ''
    if serial_number is not None and serial_number != '':
        s_serial_number = f""" and serial_number = :serial_number """

    sql = """select id, serial_number, name, type, lon, lat, scene_id, element_type, parent_id, info 
              from element 
              where 1=1 """ + s_id + s_scene_id + s_element_type + s_serial_number + """ order by serial_number, id """

    sql_count = get_sql(sql, sql_content='count')
    sql = get_sql(sql, sql_content='detail')
    rows = db.engine.execute(
        text(sql).params(limit=limit, offset=offset, id=id, scene_id=scene_id, element_type=element_type,
                         serial_number=serial_number))
    if limit is None and offset == 0:
        count = rows.rowcount
    else:
        count = db.engine.execute(
            text(sql_count).params(id=id, scene_id=scene_id, element_type=element_type,
                                   serial_number=serial_number)).first()[
            0]

    data = []
    for row in rows:
        element = Element(id=row['id'], serial_number=row['serial_number'], name=row['name'], type=row['type'],
                          lon=row['lon'], lat=row['lat'], scene_id=row['scene_id'], element_type=row['element_type'],
                          parent_id=row['parent_id'], info=row['info'])
        data.append(element)
    db.close()
    return data, count


# 新增元素数据
def insert_element_data(db, data):
    sql = text("""
    insert into 
    element(id, serial_number, name, type, lon, lat, scene_id, element_type, parent_id, info)
    values(:id, :serial_number, :name, :type, :lon, :lat, :scene_id, :element_type, :parent_id, :info)
    """).params(id=data.id, serial_number=data.serial_number, name=data.name, type=data.type, lon=data.lon,
                lat=data.lat,
                scene_id=data.scene_id, element_type=data.element_type, parent_id=data.parent_id, info=data.info)
    db.engine.execute(sql)
    db.close()
    return True


# 更新元素数据
def update_element_data(db, data):
    sql = text("""
            update element
            set 
            name=:name 
            where id=:id
            """).params(id=data.id, name=data.name)
    db.engine.execute(sql)
    db.close()
    return True


# 删除元素数据
def delete_element_data(db, id=None, scene_id=None, id_li=None):
    sign = 0
    s_id = ""
    if id is not None and id != "":
        sign = 1
        s_id = """ and id= :id """

    s_scene_id = ""
    if scene_id is not None and scene_id != "":
        sign = 1
        s_scene_id = """ and scene_id= :scene_id """

    s_id_li = ""
    if id_li is not None and id_li != "":
        sign = 1
        try:
            id_li = tuple(id_li)
            s_id_li = """ and id in :id_li """
        except:
            pass

    sql = text("""
            delete from element
            where 1=1 """ + s_id + s_scene_id + s_id_li + """
            """).params(id=id, scene_id=scene_id, id_li=id_li)
    if sign:
        db.engine.execute(sql)
        db.close()
    return True


# 获取最大序列号
def get_max_serial_number(db, element):
    s_scene_id = ''
    if element.scene_id is not None and element.scene_id != '':
        s_scene_id = f""" and scene_id = :scene_id """

    s_element_type = ''
    if element.element_type is not None and element.element_type != '':
        s_element_type = f""" and element_type = :element_type """

    s_type = ''
    if element.type is not None and element.type != '':
        s_type = f""" and type = :type """

    s_parent_id = ''
    if element.parent_id is not None and element.parent_id != '':
        s_parent_id = f""" and parent_id = :parent_id """

    sql = f"""select max(cast("serial_number" as INTEGER)) as max_serial_number
              from element where 1=1 """ + s_scene_id + s_element_type + s_type + s_parent_id + """ """
    rows = db.engine.execute(
        text(sql).params(scene_id=element.scene_id, element_type=element.element_type, type=element.type,
                         parent_id=element.parent_id))
    max_number = 0
    if rows.rowcount > 0:
        row = rows.first()
        max_number = row['max_serial_number']
        if not max_number:
            max_number = 0
    db.close()
    return max_number


# 获取元素头部数据
def get_element_header_data(db, limit=None, offset=0, id=None):
    s_id = ''
    if id is not None and id != '':
        s_id = f""" and id = :id """

    sql = """select id, header 
              from element_header 
              where 1=1 """ + s_id + """ order by id """

    sql_count = get_sql(sql, sql_content='count')
    sql = get_sql(sql, sql_content='detail')
    rows = db.engine.execute(
        text(sql).params(limit=limit, offset=offset, id=id))
    if limit is None and offset == 0:
        count = rows.rowcount
    else:
        count = db.engine.execute(
            text(sql_count).params(id=id)).first()[
            0]

    data = []
    for row in rows:
        element_header = ElementHeader(id=row['id'], header=row['header'])
        data.append(element_header)
    db.close()
    return data, count


# 判断元素头部数据是否存在
def element_header_exist(db, id=None):
    sql = text("""
            select 1 
            from element_header 
            where id=:id 
            """).params(id=id)
    rows = db.engine.execute(sql)
    db.close()
    if rows.rowcount > 0:
        return True
    return False


# 新增元素头部数据
def insert_element_header_data(db, data):
    sql = text("""
    insert into 
    element_header(id, header)
    values(:id, :header)
    """).params(id=data.id, header=data.header)
    db.engine.execute(sql)
    db.close()
    return True


# 更新元素头部数据
def update_element_header_data(db, data):
    sql = text("""
            update element_header 
            set 
            header=:header 
            where id=:id
            """).params(id=data.id, header=data.header)
    db.engine.execute(sql)
    db.close()
    return True


# 删除元素头部数据
def delete_element_header_data(db, id=None, id_li=None):
    sign = 0
    s_id = ""
    if id is not None and id != "":
        sign = 1
        s_id = """ and id= :id """

    s_id_li = ""
    if id_li is not None and id_li != "":
        sign = 1
        try:
            id_li = tuple(id_li)
            s_id_li = """ and id in :id_li """
        except:
            pass

    sql = text("""
            delete from element_header
            where 1=1 """ + s_id + s_id_li + """
            """).params(id=id, id_li=id_li)
    if sign:
        db.engine.execute(sql)
        db.close()
    return True


# 获取元素参数数据
def get_element_param_data(db, limit=None, offset=0, id=None):
    s_id = ''
    if id is not None and id != '':
        s_id = f""" and id = :id """

    sql = """select id, row_index, col_index, value 
              from element_param 
              where 1=1 """ + s_id + """ order by id, row_index, col_index """

    sql_count = get_sql(sql, sql_content='count')
    sql = get_sql(sql, sql_content='detail')
    rows = db.engine.execute(
        text(sql).params(limit=limit, offset=offset, id=id))
    if limit is None and offset == 0:
        count = rows.rowcount
    else:
        count = db.engine.execute(
            text(sql_count).params(id=id)).first()[0]

    data = []
    for row in rows:
        element_param = ElementParam(id=row['id'], row_index=row['row_index'], col_index=row['col_index'],
                                     value=row['value'])
        data.append(element_param)
    db.close()
    return data, count


# 新增元素参数数据
def insert_element_param_data(db, data):
    sql = text("""
    insert into 
    element_param(id, row_index, col_index, value)
    values(:id, :row_index, :col_index, :value)
    """).params(id=data.id, row_index=data.row_index, col_index=data.col_index, value=data.value)
    db.engine.execute(sql)
    db.close()
    return True


# 批量新增元素参数数据
def batch_insert_element_param_data(db, model_data_li):
    add_sql = ""
    sql = """
    insert into 
    element_param(id, row_index, col_index, value)
    values """
    k = 4
    i = 0
    data_dic = {}
    for row in model_data_li:
        add_sql += f"""
        (:data{i*k+0}, :data{i*k+1}, :data{i*k+2}, :data{i*k+3}),"""
        data_dic[f'data{i*k+0}'] = row.id
        data_dic[f'data{i*k+1}'] = row.row_index
        data_dic[f'data{i*k+2}'] = row.col_index
        data_dic[f'data{i*k+3}'] = row.value
        i += 1
    insert_count = 0
    if add_sql.__contains__(","):
        add_sql = add_sql[:-1]
        add_sql += ";"
        rows = db.engine.execute(text(sql + add_sql).params(**data_dic))
        insert_count = rows.rowcount
    db.close()
    return insert_count


# 删除元素参数数据
def delete_element_param_data(db, id=None, id_li=None):
    sign = 0
    s_id = ""
    if id is not None and id != "":
        sign = 1
        s_id = """ and id= :id """

    s_id_li = ""
    if id_li is not None and id_li != "":
        sign = 1
        try:
            id_li = tuple(id_li)
            s_id_li = """ and id in :id_li """
        except:
            pass

    sql = text("""
            delete from element_param
            where 1=1 """ + s_id + s_id_li + """
            """).params(id=id, id_li=id_li)
    if sign:
        db.engine.execute(sql)
        db.close()
    return True


# 获取元素参数中最大的行列索引
def get_max_index(db, id=None):
    sql = f"""select max(cast("row_index" as INTEGER)) as max_row_index, max(cast("col_index" as INTEGER)) as max_col_index
              from element_param where id=:id """
    rows = db.engine.execute(
        text(sql).params(id=id))
    row = rows.first()
    max_row_index = row['max_row_index']
    max_col_index = row['max_col_index']
    if max_row_index is None or max_col_index is None:
        max_row_index = -1
        max_col_index = -1
    db.close()
    return max_row_index, max_col_index
