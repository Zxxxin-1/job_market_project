> 项目名称：Python招聘岗位爬虫与就业知识图谱
> 项目：人工智能与数据科学就业市场知识图谱构建及就业趋势可视化分析

## 环境要求
- Python >= 3.9
- MySQL 8.0+
- Neo4j 数据库（版本推荐 4.4 / 5.x）
- Git
- 操作系统：Windows

## 1. 获取项目代码
```bash
git clone https://github.com/Zxxxin-1/job_market_project.git
cd job_market_project
```

## 2. 创建并激活虚拟环境

```
# Windows CMD / PowerShell
python -m venv venv
venv\Scripts\activate
```

> 
> ✅ 激活成功标志：命令行前缀会出现 `(venv)`

## 3. 安装项目依赖包

```
# 使用清华源加速下载
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 4. 数据库准备

### 4.1 MySQL 准备

1. 本地安装并启动 MySQL 服务
2. 在`config.py`中，修改 MySQL 连接配置：数据库地址、用户名、密码、数据库名
3. 执行初始化脚本，自动创建岗位、企业、技能、薪资相关数据表

### 4.2 Neo4j 准备

1. 启动 Neo4j 服务（桌面版 Neo4j Desktop 打开对应数据库实例）
2. 在`config.py`中修改 Neo4j 连接配置：URI、账号、密码、数据库名称
3. 确认 Neo4j 默认端口 `7687`，防火墙放行该端口

## 5. 项目启动【按顺序执行】

```
# 1. MySQL初始化，自动建表
python init_mysql.py

# 2. 爬虫采集岗位数据，存入MySQL
python spider_data.py

# 3. 读取MySQL数据，构建Neo4j知识图谱
python build_neo4j_kg.py

# 4. 数据分析统计，生成统计结果文件
python analysis.py

# 5. 启动Flask后端Web服务
python app.py
```

## 6. 访问 Web 可视化看板

浏览器打开：[http://127.0.0.1:8080]
页面包含：知识图谱可视化、岗位地域分布、薪资统计、技能热度图表。

## 7. 项目关闭

1. 终端按 `Ctrl + C` 停止 Flask 后端、爬虫程序
2. 退出 Python 虚拟环境

```
deactivate
```

## 常见问题排查

1. **虚拟环境激活失败**
Windows 终端切换为 CMD，或者 VSCode 开启开发者模式；PowerShell 需要开启执行权限。
2. **pip 安装包报错**
检查网络，更换清华源；部分包安装失败可以单独执行`pip install 包名`单独安装。
3. **MySQL 连接失败**
确认 MySQL 服务已经启动；核对 config.py 内账号密码；数据库提前创建。
4. **Neo4j 连接失败**
核对账号密码；确认 Neo4j 实例已启动；端口 7687 没有被防火墙拦截。
5. **端口 8080 被占用**
修改`app.py`里面 Flask 服务端口号，改为 5001 等其他空闲端口。
6. **知识图谱无数据**
确认爬虫已经成功采集数据存入 MySQL；build_neo4j_kg.py 执行无报错。