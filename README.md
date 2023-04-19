## 智能农机管理
### 大唐杯训练项目
---
基于'PgSQL'数据库的全栈管理/控制系统，面相智能化农业机械设备，
依托于5G的快速发展，将产品接入5G网络，拥有常规WLAN无法比拟的
超大带机量、超低通信延迟。

### 项目进度
- [x] 建立数据库操作API接口，实现对表和DATA的'新建'/'编辑'
- [ ] 建立简单的前端界面
- [ ] 前端接入API接口，实现数据操作
- [ ] 传入更多数据'实时天气'等，实现自动化录入
- [ ] Unknow
- [ ] *大饼*引入控制算法，实现自动作业规划

### 结构目录
| ./lib/`pgsql.py` #基于psycopg2的数据库操作 </p>
| -----/`api.py` #基于fastapi建立web—api </p>
| ./src/`xxx.json` #数据存储目录 </p>
| ./web/`app.vue` #前端目录 </p>

### 项目依赖
#### python_models
- pydantic
- fastapi[full]
- psycopg2-binary
#### node.js
- vue@latest

### 技术栈
#### TODO
- [x] 连接数据库，熟悉常见表操作
- [ ] 熟悉FASTAPI基本函数
- [ ] 熟悉SQLAlchemy基本函数
- [ ] 简要学习HTML\CSS\JavaScript
- [ ] 大概了解Vue3基本结构
- [ ] \可选\ 熟悉pydantic基本函数，数据类型
