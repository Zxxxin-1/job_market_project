#  job_market_project
人工智能与数据科学就业市场知识图谱构建及就业趋势可视化分析

##  项目简介
本项目基于Python实现招聘岗位信息爬虫，采集互联网招聘岗位、企业、技能、薪资、地域数据，存入MySQL关系数据库；利用Neo4j图数据库构建就业多维度知识图谱。通过Python完成数据分析挖掘行业需求特征，基于Flask搭建后端服务，使用ECharts实现Web可视化看板，完成岗位地域分布、薪资水平、技能热度等就业趋势分析。

##  项目功能
1. 招聘数据爬虫：自动采集岗位信息，日志记录接口访问、数据处理全过程
2. MySQL存储：保存岗位、企业、技能、城市、薪资结构化招聘数据
3. Neo4j知识图谱：构建岗位、企业、技能、城市节点与关联关系
4. 数据分析：统计岗位分布、薪资、技能热度，挖掘行业就业特征
5. Web可视化看板：
    - 知识图谱力导向图展示实体关联
    - 各城市岗位数量柱状图
    - 城市平均薪资柱状图
    - 技能需求热度TOP10图表
    - 薪资区间分布饼图

##  技术栈
- 编程语言：Python 3.9+
- 数据采集：requests、BeautifulSoup、logging日志系统
- 数据库：MySQL（关系数据）、Neo4j（图数据库/知识图谱）
- 数据分析：Pandas、NumPy
- Web后端：Flask
- 前端可视化：HTML、ECharts
- 协作工具：Git + GitHub

##  团队分工
- 张鑫：Neo4j图数据库，知识图谱构建脚本开发（负责全项目代码整合、模块对接，联调各模块接口，保证整套程序可完整串联运行）
- 李哲：MySQL数据库初始化，招聘数据采集入库
- 陈智鸿：数据分析模块，全局配置文件、日志工具封装
- 康哲溢：Flask后端接口、Web前端可视化看板开发

##  项目目录结构

job_market_project/
├── pycache/             # Python 自动生成缓存文件（git 忽略不上传）
├── data/                # 临时数据存放目录
│   ├── .gitkeep
│   └── ai_ds_jobs.csv   # 导出岗位 csv 数据
├── docs/                # 项目文档、答辩截图、Cypher 语句
│   ├── .gitkeep
│   └── kg_cypher.txt    # Neo4j 查询语句
├── logs/                # 程序运行日志目录
├── static/              # Web 静态资源
│   └── .gitkeep
├── temp_output/         # 数据分析输出文件
│   ├── .gitkeep
│   └── sample_stats.json # 分析统计结果 json
├── templates/
│   ├── .gitkeep
│   └── dashboard.html   # 可视化看板页面
├── .gitignore
├── analysis.py          # 数据分析脚本
├── app.py               # Flask 后端入口
├── build_neo4j_kg.py    # Neo4j 知识图谱构建
├── config.py            # 全局配置（数据库账号密码）
├── gen_data.py          # 模拟测试数据
├── init_mysql.py        # MySQL 数据表初始化
├── logger_util.py       # 日志工具模块
├── README.md            # 项目介绍文档（本文件）
├── requirements.txt     # Python 依赖包清单
├── RUN.md               # 项目部署运行指南
├── spider_data.py       # 招聘爬虫脚本
└── test_case.py         # 单元测试



## 快速启动
完整部署步骤请查看：**RUN.md**
```bash
# 简单命令预览
python init_mysql.py
python spider_data.py
python build_neo4j_kg.py
python analysis.py
python app.py
```

浏览器访问：[http://127.0.0.1:8080]