## 智能农机管理
### 大唐杯训练项目
---
基于'PgSQL'数据库的全栈管理/控制系统，面相智能化农业机械设备，
依托于5G的快速发展，将产品接入5G网络，拥有常规WLAN无法比拟的
超大带机量、超低通信延迟。


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

### TODO
- [x] 连接数据库，熟悉常见表操作
- [ ] 熟悉FASTAPI基本函数
- [ ] 熟悉SQLAlchemy基本函数
- [ ] 简要学习HTML\CSS\JavaScript
- [ ] 大概了解Vue3基本结构
- [ ] \可选\ 熟悉pydantic基本函数，数据类型
