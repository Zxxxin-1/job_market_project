from neo4j import GraphDatabase, basic_auth
from config import NEO4J_CONFIG
NEO4J_URI = NEO4J_CONFIG["uri"]
NEO4J_USER = NEO4J_CONFIG["user"]
NEO4J_PWD = NEO4J_CONFIG["password"]
from logger_util import logger

mock_job_data = [
    {
        "id": 1,
        "job_name": "Python开发工程师",
        "company_name": "字节跳动",
        "city": "北京",
        "salary_min": 15000,
        "salary_max": 25000,
        "experience": "3-5年",
        "education": "本科",
        "skill_tags": ["Python", "MySQL", "Redis", "Docker"],
        "industry": "互联网"
    },
    {
        "id": 2,
        "job_name": "前端开发工程师",
        "company_name": "腾讯",
        "city": "深圳",
        "salary_min": 12000,
        "salary_max": 20000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Vue", "JavaScript", "HTML", "CSS"],
        "industry": "互联网"
    },
    {
        "id": 3,
        "job_name": "Java后端开发工程师",
        "company_name": "阿里巴巴",
        "city": "杭州",
        "salary_min": 18000,
        "salary_max": 30000,
        "experience": "3-5年",
        "education": "本科",
        "skill_tags": ["Java", "SpringBoot", "MySQL", "RocketMQ"],
        "industry": "互联网"
    },
    {
        "id": 4,
        "job_name": "大数据开发工程师",
        "company_name": "网易",
        "city": "杭州",
        "salary_min": 16000,
        "salary_max": 28000,
        "experience": "3-5年",
        "education": "本科",
        "skill_tags": ["Hadoop", "Spark", "Flink", "Hive"],
        "industry": "互联网"
    },
    {
        "id": 5,
        "job_name": "测试开发工程师",
        "company_name": "美团",
        "city": "北京",
        "salary_min": 13000,
        "salary_max": 22000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Python", "Selenium", "Postman", "Linux"],
        "industry": "互联网"
    },
    {
        "id": 6,
        "job_name": "Go后端开发工程师",
        "company_name": "快手",
        "city": "北京",
        "salary_min": 20000,
        "salary_max": 35000,
        "experience": "3-5年",
        "education": "本科",
        "skill_tags": ["Golang", "gRPC", "MySQL", "K8s"],
        "industry": "互联网"
    },
    {
        "id": 7,
        "job_name": "数据分析工程师",
        "company_name": "拼多多",
        "city": "上海",
        "salary_min": 14000,
        "salary_max": 24000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Python", "Pandas", "SQL", "Matplotlib"],
        "industry": "互联网"
    },
    {
        "id": 8,
        "job_name": "运维工程师",
        "company_name": "京东",
        "city": "北京",
        "salary_min": 11000,
        "salary_max": 18000,
        "experience": "1-3年",
        "education": "大专",
        "skill_tags": ["Linux", "Shell", "Docker", "Nginx"],
        "industry": "互联网"
    },
    {
        "id": 9,
        "job_name": "人工智能算法工程师",
        "company_name": "百度",
        "city": "北京",
        "salary_min": 22000,
        "salary_max": 40000,
        "experience": "3-5年",
        "education": "硕士",
        "skill_tags": ["Python", "TensorFlow", "PyTorch", "深度学习"],
        "industry": "人工智能"
    },
    {
        "id": 10,
        "job_name": "产品经理",
        "company_name": "小米",
        "city": "北京",
        "salary_min": 10000,
        "salary_max": 18000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Axure", "需求分析", "原型设计", "数据分析"],
        "industry": "互联网"
    },
    {
        "id": 11,
        "job_name": "移动端Android开发",
        "company_name": "vivo",
        "city": "东莞",
        "salary_min": 12000,
        "salary_max": 22000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Java", "Kotlin", "Android", "SDK"],
        "industry": "智能硬件"
    },
    {
        "id": 12,
        "job_name": "iOS开发工程师",
        "company_name": "OPPO",
        "city": "东莞",
        "salary_min": 13000,
        "salary_max": 23000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Swift", "Objective-C", "Xcode"],
        "industry": "智能硬件"
    },
    {
        "id": 13,
        "job_name": "网络安全工程师",
        "company_name": "奇安信",
        "city": "北京",
        "salary_min": 14000,
        "salary_max": 26000,
        "experience": "3-5年",
        "education": "本科",
        "skill_tags": ["渗透测试", "防火墙", "漏洞挖掘", "Linux"],
        "industry": "网络安全"
    },
    {
        "id": 14,
        "job_name": "爬虫开发工程师",
        "company_name": "知乎",
        "city": "北京",
        "salary_min": 12000,
        "salary_max": 20000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Python", "Scrapy", "Requests", "反爬"],
        "industry": "互联网"
    },
    {
        "id": 15,
        "job_name": "云计算工程师",
        "company_name": "阿里云",
        "city": "杭州",
        "salary_min": 16000,
        "salary_max": 28000,
        "experience": "3-5年",
        "education": "本科",
        "skill_tags": ["AWS", "阿里云", "Docker", "K8s"],
        "industry": "云计算"
    },
    {
        "id": 16,
        "job_name": "数据库工程师",
        "company_name": "腾讯云",
        "city": "深圳",
        "salary_min": 17000,
        "salary_max": 29000,
        "experience": "3-5年",
        "education": "本科",
        "skill_tags": ["MySQL", "Redis", "MongoDB", "数据库调优"],
        "industry": "云计算"
    },
    {
        "id": 17,
        "job_name": "游戏开发工程师",
        "company_name": "米哈游",
        "city": "上海",
        "salary_min": 18000,
        "salary_max": 32000,
        "experience": "3-5年",
        "education": "本科",
        "skill_tags": ["C++", "Unity", "Shader", "游戏引擎"],
        "industry": "游戏"
    },
    {
        "id": 18,
        "job_name": "UI设计师",
        "company_name": "B站",
        "city": "上海",
        "salary_min": 9000,
        "salary_max": 16000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Figma", "PS", "交互设计", "视觉设计"],
        "industry": "互联网"
    },
    {
        "id": 19,
        "job_name": "售前技术工程师",
        "company_name": "华为",
        "city": "深圳",
        "salary_min": 10000,
        "salary_max": 19000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["网络架构", "方案设计", "服务器", "云计算"],
        "industry": "通信设备"
    },
    {
        "id": 20,
        "job_name": "BI数据可视化工程师",
        "company_name": "携程",
        "city": "上海",
        "salary_min": 13000,
        "salary_max": 21000,
        "experience": "1-3年",
        "education": "本科",
        "skill_tags": ["Python", "ECharts", "Tableau", "数据大屏"],
        "industry": "互联网"
    }
]


def clear_graph(session):
    """清空图谱所有节点与关系"""
    cypher = "MATCH (n) DETACH DELETE n;"
    session.run(cypher)
    logger.info("图谱已清空")


def create_job_node(session, job):
    """创建岗位节点（完整字段）"""
    cypher = """
    MERGE (j:Job{
        id:$id,
        job_name:$job_name,
        salary_min:$salary_min,
        salary_max:$salary_max,
        experience:$experience,
        education:$education,
        industry:$industry
    })
    """
    session.run(cypher, parameters=job)


def create_company_relation(session, job):
    """公司节点 + 岗位归属关系"""
    cypher = """
    MERGE (c:Company{name:$company_name})
    MERGE (j:Job{id:$id})-[:BELONG_TO]->(c)
    """
    params = {"company_name": job["company_name"], "id": job["id"]}
    session.run(cypher, parameters=params)


def create_city_relation(session, job):
    """城市节点 + 岗位地理位置关系"""
    cypher = """
    MERGE (city:City{name:$city})
    MERGE (j:Job{id:$id})-[:LOCATED_IN]->(city)
    """
    params = {"city": job["city"], "id": job["id"]}
    session.run(cypher, parameters=params)


def create_skill_relation(session, job):
    """技能节点 + 岗位技能需求关系"""
    job_id = job["id"]
    for skill_name in job["skill_tags"]:
        cypher = """
        MERGE (s:Skill{name:$skill_name})
        MERGE (j:Job{id:$job_id})-[:REQUIRE_SKILL]->(s)
        """
        params = {"skill_name": skill_name, "job_id": job_id}
        session.run(cypher, parameters=params)


def count_graph_stat(session):
    """图谱数据统计汇总"""
    total_nodes = session.run("MATCH(n) RETURN count(n) AS total").single()["total"]
    total_rels = session.run("MATCH ()-[r]->() RETURN count(r) AS total").single()["total"]
    job_num = session.run("MATCH (j:Job) RETURN count(j) AS num").single()["num"]
    company_num = session.run("MATCH (c:Company) RETURN count(c) AS num").single()["num"]
    city_num = session.run("MATCH (city:City) RETURN count(city) AS num").single()["num"]
    skill_num = session.run("MATCH (s:Skill) RETURN count(s) AS num").single()["num"]
    logger.info(f"图谱构建统计完成：")
    logger.info(f"总节点数：{total_nodes} | 总关系数：{total_rels}")
    logger.info(f"岗位数：{job_num} | 公司数：{company_num} | 城市数：{city_num} | 技能数：{skill_num}")


def build_graph(job_list):
    """图谱构建主函数"""
    driver = None
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PWD))
        logger.info("开始连接Neo4j数据库")
        with driver.session() as session:
            clear_graph(session)
            total = len(job_list)
            success_count = 0
            for job in job_list:
                try:
                    create_job_node(session, job)
                    create_company_relation(session, job)
                    create_city_relation(session, job)
                    create_skill_relation(session, job)
                    success_count += 1
                    logger.info(f"岗位 {job['job_name']} 图谱构建完成 ({success_count}/{total})")
                except Exception as e:
                    logger.error(f"岗位【{job['job_name']}】构建失败，跳过本条：{str(e)}", exc_info=True)
            count_graph_stat(session)
            logger.info(f"图谱构建结束：成功 {success_count}/{total}")
    except Exception as e:
        logger.error(f"图谱构建整体失败：{str(e)}", exc_info=True)
    finally:
        if driver:
            driver.close()
            logger.info("Neo4j连接已关闭")


def load_data_from_mysql(rows: list[dict] = None) -> list[dict]:
    """
    从MySQL读取KG原始数据【预留对接接口】
    :param rows: 预留参数，李哲传入mysql查询结果 list[dict]
                 rows=None时使用本地mock数据调试
    :return: 标准化岗位列表，直接供给build_graph使用
    """
    if rows is not None:
        logger.info("收到外部传入MySQL真实数据")
        return rows

    logger.info("当前加载Mock模拟岗位数据，等待李哲MySQL接口对接")
    return mock_job_data


if __name__ == "__main__":
    # 李哲完成后，只需要把她查询得到的mysql_rows传入：
    # mysql_rows = get_mysql_data_from_lizhe()
    # data = load_data_from_mysql(rows=mysql_rows)
    data = load_data_from_mysql()
    build_graph(data)
