# 项目运行指南
> 项目：Python招聘岗位爬虫与就业知识图谱

## 环境要求
- Python >= 3.9
- Neo4j 数据库（版本推荐 4.4 / 5.x）
- Git
- 操作系统：Windows

## 1. 获取项目代码
```bash
git clone 你的项目仓库地址
cd 项目文件夹名称
```

## 2. 创建并激活虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```
> 激活成功后，命令行前缀会出现 `(venv)`

## 3. 安装项目依赖包
```bash
# 使用清华源加速下载
pip install -r requirements.txt -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)
```

## 4. Neo4j 数据库准备
1. 启动 Neo4j 服务
2. 创建数据库实例，修改配置文件内的 neo4j 账号、密码、数据库名称
3. 确认数据库端口默认 `7687` 可访问

## 5. 项目启动
```bash
# 1. MySQL初始化（李哲）
python init_mysql.py
# 2. 启动爬虫/数据入库（李哲）
python spider_data.py
# 3. 构建Neo4j知识图谱（张鑫）
python build_neo4j_kg.py
# 4. 启动Flask后端服务（康哲溢）
python app.py
```

## 6. 访问Web服务
浏览器打开：[http://127.0.0.1:5000](http://127.0.0.1:5000)

## 常见问题排查
1. 虚拟环境激活失败：Windows终端切换为CMD，或开启开发者模式
2. pip安装包报错：检查网络，更换清华源；部分包安装失败可单独pip安装
3. Neo4j连接失败：核对账号密码、确认Neo4j服务已经启动、端口没有被防火墙拦截
4. 端口5000占用：修改main.py中的服务端口号

## 项目关闭
1. Ctrl + C 停止Flask/爬虫程序
2. 退出虚拟环境：
```bash
deactivate
```
