import datetime
import json
import logging.handlers
import os
import socket
import uuid

from flask import Flask, request, g, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine

from app.src.dao.element import *
from app.src.util.common import to_json, get_limit_offset, data_judge
from app.src.services.element import *

base_data_folder = os.environ.get('POWERGRID_IMAGE_BASE_DIR', ".")

log_folder = os.path.join(base_data_folder, "log")
if not os.path.exists(base_data_folder):
    os.mkdir(base_data_folder)
if not os.path.exists(log_folder):
    os.mkdir(log_folder)


def beijing(sec):
    beijing_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return beijing_time.timetuple()


hostname = socket.gethostname()
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(module)s] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
formatter.converter = beijing
time_rotating_handler = logging.handlers.TimedRotatingFileHandler(
    os.path.join(log_folder, 'run-{}.log'.format(hostname)), when='MIDNIGHT', interval=1, backupCount=30,
    encoding="utf8", delay=False)
time_rotating_handler.setLevel(logging.DEBUG)

# 此处配置数据库连接信息，按照数据库安装情况填写
engine = create_engine('postgresql://postgres:aKtALRFAKCRC@81.68.157.7:5432/postgres', echo=True)
db = engine.connect()

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.before_request
def before_request():
    g.requestId = str(uuid.uuid4().hex)


@app.after_request
def after_request(response):
    logger.info(json.dumps({
        "AccessLog": {
            "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-IP', request.remote_addr),
            "url": request.url,
            # "data": json.dumps(request.data),
            "requestId": g.requestId
        }
    }, ensure_ascii=False))
    return response


@app.route('/', methods=['GET', 'POST'])
def hello():
    print('/')
    print(request.form)
    return "hello {}".format(g.requestId)


# 场景查询
@app.route('/scene/select', methods=['GET', 'POST'])
def scene_select():
    data = get_scene_data(db)
    return jsonify({'code': 200, 'data': to_json(data)})


# 元素查询
@app.route('/element/select', methods=['GET', 'POST'])
def element_select():
    param = request.form
    id = param.get('id')
    element_type = param.get('element_type')
    scene_id = param.get('scene_id')
    serial_number = param.get('serial_number')
    page = param.get("page")
    limit = param.get("limit")
    limit, offset = get_limit_offset(page, limit)
    data, count = get_element_data(db, limit=limit, offset=offset, id=id, scene_id=scene_id, element_type=element_type,
                                   serial_number=serial_number)
    return jsonify({'code': 200, 'data': to_json(data), 'count': count})


# 元素保存
@app.route('/element/save', methods=['GET', 'POST'])
def element_save():
    param = request.form
    name = param.get('name')
    type = param.get('type')
    lon = param.get('lon')
    lat = param.get('lat')
    scene_id = param.get('scene_id')
    element_type = param.get('element_type')
    parent_id = param.get('parent_id')
    info = param.get('info')
    element = Element(name=name, type=type, lon=lon, lat=lat, scene_id=scene_id,
                      element_type=element_type, parent_id=parent_id, info=info)
    if 'id' in param.keys():
        element.id = param.get('id')
        update_element_data(db, data=element)
    else:
        element.serial_number = create_serial_number(db, element)
        element.id = str(uuid.uuid4().hex)
        insert_element_data(db, data=element)
    return jsonify({'code': 200, 'element': to_json(element)})


# 元素删除
@app.route('/element/delete', methods=['GET', 'POST'])
def element_delete():
    param = request.form
    id = param.get('id')
    scene_id = param.get('scene_id')
    delete_element_tree(db, id=id, scene_id=scene_id)
    return jsonify({'code': 200})


# 元素开发树结构数据
@app.route('/element/develop', methods=['GET', 'POST'])
def element_develop():
    param = request.form
    scene_id = param.get('scene_id')
    data = element_develop_data(db, scene_id=scene_id)
    return jsonify({'code': 200, 'data': to_json(data)})


# 元素头部查询
@app.route('/element/header/select', methods=['GET', 'POST'])
def element_header_select():
    param = request.form
    id = param.get('id')
    data, count = get_element_header_data(db, id=id)
    header = []
    if data:
        header = data[0].header
    return jsonify({'code': 200, 'data': to_json(header)})


# 元素头部保存
@app.route('/element/header/save', methods=['GET', 'POST'])
def element_header_save():
    param = request.form
    id = param.get('id')
    header = param.get('header')
    element_header = ElementHeader(id=id, header=header)
    if element_header_exist(db, id=id):
        update_element_header_data(db, data=element_header)
    else:
        insert_element_header_data(db, data=element_header)
    return jsonify({'code': 200})


# 元素参数查询
@app.route('/element/param/select', methods=['GET', 'POST'])
def element_param_select():
    param = request.form
    id = param.get('id')
    data = element_param_data_select_deal(db, id=id)
    return jsonify({'code': 200, 'data': to_json(data)})


# 元素参数查询
@app.route('/element/param/save', methods=['GET', 'POST'])
def element_param_save():
    param = request.form
    id = param.get('id')
    try:
        data = json.loads(param.get('data'))
    except:
        return jsonify({'code': 0})
    element_param_data_save_deal(db, id=id, data_lis=data)
    return jsonify({'code': 200})


logger.info("{} 启动成功".format(datetime.datetime.now()))
