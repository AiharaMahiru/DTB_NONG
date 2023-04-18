from app.src.util.common import get_without_none


# 场景模型
class Scene:
    def __init__(self, scene_id=None, name=None):
        self.scene_id = get_without_none(scene_id)
        self.name = get_without_none(name)


# 元素模型
class Element:
    def __init__(self, id=None, serial_number=None, name=None, type=None, lon=None, lat=None, scene_id=None, info=None,
                 element_type=None, parent_id=None):
        self.id = get_without_none(id)
        self.serial_number = get_without_none(serial_number)
        self.name = get_without_none(name)
        self.type = get_without_none(type)
        self.lon = get_without_none(lon)
        self.lat = get_without_none(lat)
        self.scene_id = get_without_none(scene_id)
        self.element_type = get_without_none(element_type)
        self.parent_id = get_without_none(parent_id)
        self.info = get_without_none(info)


# 元素头部模型
class ElementHeader:
    def __init__(self, id=None, header=None):
        self.id = get_without_none(id)
        self.header = get_without_none(header)


# 元素参数模型
class ElementParam:
    def __init__(self, id=None, row_index=None, col_index=None, value=None):
        self.id = get_without_none(id)
        self.row_index = get_without_none(row_index)
        self.col_index = get_without_none(col_index)
        self.value = get_without_none(value)
