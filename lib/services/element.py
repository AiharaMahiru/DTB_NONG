from app.src.dao.element import *
import copy


# 递归获取所有子元素id
def get_tree_id_li(element_tree_li, pid=''):
    data_li = []
    if not element_tree_li:
        return data_li
    element_tree_li_cp = element_tree_li.copy()
    for element_tree in element_tree_li:
        if element_tree.parent_id == pid:
            data_li.append(element_tree.id)
            element_tree_li_cp.remove(element_tree)
            ret_li = get_tree_id_li(element_tree_li_cp, pid=element_tree.id)
            data_li.extend(ret_li)
    return data_li


# 删除元素数据及子数据
def delete_element_tree(db, id=None, scene_id=None):
    data_li, count = get_element_data(db, scene_id=scene_id)
    tree_id_li = get_tree_id_li(data_li, pid=id)
    tree_id_li.append(id)
    delete_element_data(db, id_li=tree_id_li)
    delete_element_header_data(db, id_li=tree_id_li)
    delete_element_param_data(db, id_li=tree_id_li)
    return True


# 生成当前类型元素最大序号
def create_serial_number(db, element):
    serial_number = get_max_serial_number(db=db, element=element) + 1
    return serial_number


# 递归使元素列表装换成树结构
def element_tree_deal(element_trees, pid=''):
    data_li = []
    if not element_trees:
        return data_li
    element_trees_cp = element_trees.copy()
    for element_tree in element_trees:
        if element_tree.parent_id == pid:
            data_li.append(element_tree)
            element_trees_cp.remove(element_tree)
            ret_li = element_tree_deal(element_trees_cp, pid=element_tree.id)
            element_tree.children = ret_li
    return data_li


# 元素数据分类处理
def element_develop_data(db, scene_id=None):
    data_li, count = get_element_data(db, scene_id=scene_id)
    data_trees = element_tree_deal(element_trees=data_li)
    data_dic = {
        'base_station': [],
        'terminal': []
    }
    for data_tree in data_trees:
        if data_tree.element_type == '基站库':
            data_dic['base_station'].append(data_tree)
        elif data_tree.element_type == '终端库':
            data_dic['terminal'].append(data_tree)
    return data_dic


# 元素参数格式化处理
def element_param_data_select_deal(db, id=None):
    data_li, count = get_element_param_data(db, id=id)
    max_row_index = -1
    max_col_index = -1
    if data_li:
        max_row_index = max([data.row_index for data in data_li])
        max_col_index = max([data.col_index for data in data_li])
    ret_li = []
    for i in range(max_row_index + 1):
        li = []
        for j in range(max_col_index + 1):
            li.append('')
        ret_li.append(li)
    for data in data_li:
        ret_li[int(data.row_index)][int(data.col_index)] = data.value
    return ret_li


# 元素参数格式化保存
def element_param_data_save_deal(db, id=None, data_lis=None):
    save_li = []
    for i, data_li in enumerate(data_lis):
        for j, data in enumerate(data_li):
            save_li.append(ElementParam(id=id, row_index=i, col_index=j, value=data))
    delete_element_param_data(db, id=id)
    batch_insert_element_param_data(db, save_li)
