# config.py 数据库配置
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "填写自己本机mysql密码",
    "database": "job_market_db",
    "charset": "utf8mb4"
}

NEO4J_CONFIG = {
    "uri": "bolt://127.0.0.1:7687",
    "user": "neo4j",
    "password": "填写自己本机neo4j密码"
}
