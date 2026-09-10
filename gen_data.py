import pandas as pd
import random
import os
import pymysql
from config import MYSQL_CONFIG
from logger_util import logger

# 创建data文件夹
if not os.path.exists("./data"):
    os.makedirs("./data")

# 模拟数据池
job_list = ["数据分析师","数据开发工程师","算法工程师","AI大模型工程师","机器学习工程师","BI工程师"]
company_list = ["字节跳动","腾讯","阿里","百度","科大讯飞","海康威视","网易","美团"]
city_list = ["北京","上海","深圳","杭州","广州","南京","大连","成都","武汉"]
exp_list = ["应届生","1‑3年","3‑5年","5‑10年"]
edu_list = ["本科","硕士","大专"]
skill_list = [
    "Python,SQL,Pandas",
    "Python,Tensorflow,Pytorch",
    "SQL,Hive,Spark",
    "Python,大模型,LangChain",
    "Java,MySQL,Kafka",
    "Python,数据可视化"
]
industry_list = ["互联网","人工智能","金融","智能制造","软件服务"]
# 福利池，英文逗号分隔
welfare_list = [
    "五险一金,双休",
    "年终奖,带薪年假",
    "餐补,交通补贴",
    "五险一金,节日福利",
    "",  # 部分岗位无福利
    "绩效奖金,弹性工作制"
]

rows = []
for _ in range(250):
    job_name = random.choice(job_list)
    company_name = random.choice(company_list)
    city = random.choice(city_list)
    salary_min = random.randint(8,22)
    salary_max = salary_min + random.randint(3,12)
    exp = random.choice(exp_list)
    edu = random.choice(edu_list)
    skill = random.choice(skill_list)
    ind = random.choice(industry_list)
    welfare = random.choice(welfare_list)

    rows.append({
        "job_name": job_name,
        "company_name": company_name,
        "city": city,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "experience": exp,
        "education": edu,
        "skill_tags": skill,
        "industry": ind,
        "welfare": welfare
    })

df = pd.DataFrame(rows)
csv_path = "./data/ai_ds_jobs.csv"
df.to_csv(csv_path, encoding="utf‑8‑sig", index=False)
logger.info(f"✅数据集生成完毕，路径 {csv_path}，共 {len(df)} 条")


def create_job_raw_table():
    """新建job_raw原始数据表"""
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"],
            charset="utf8mb4"
        )
        cursor = conn.cursor()
        create_sql = """
        CREATE TABLE IF NOT EXISTS `job_raw` (
            `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键id',
            `job_name` VARCHAR(255) COMMENT '岗位名称',
            `company_name` VARCHAR(255) COMMENT '公司名称',
            `salary_min` INT NULL COMMENT '最低薪资(k)',
            `salary_max` INT NULL COMMENT '最高薪资(k)',
            `city` VARCHAR(100) COMMENT '城市',
            `education` VARCHAR(100) COMMENT '学历',
            `experience` VARCHAR(100) COMMENT '工作经验',
            `skill_tags` TEXT COMMENT '技能，英文逗号分隔',
            `industry` VARCHAR(255) COMMENT '行业',
            `welfare` TEXT COMMENT '福利，英文逗号分隔'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原始250条岗位模拟数据表';
        """
        cursor.execute(create_sql)
        conn.commit()
        logger.info("✅ job_raw 表创建/校验完成")
    except Exception as e:
        logger.error(f"建表失败：{e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_csv_to_mysql():
    """把生成的csv批量插入job_raw"""
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"],
            charset="utf8mb4"
        )
        cursor = conn.cursor()
        insert_sql = """
        INSERT INTO job_raw(job_name,company_name,salary_min,salary_max,city,education,experience,skill_tags,industry,welfare)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        data_list = []
        for _, row in df.iterrows():
            data_list.append((
                row["job_name"],
                row["company_name"],
                row["salary_min"],
                row["salary_max"],
                row["city"],
                row["education"],
                row["experience"],
                row["skill_tags"],
                row["industry"],
                row["welfare"]
            ))
        cursor.executemany(insert_sql, data_list)
        conn.commit()
        logger.info(f"✅成功插入 {len(data_list)} 条数据到 job_raw")
    except Exception as e:
        logger.error(f"插入失败：{e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_job_list_from_job_raw():
    """
    【对外接口】读取job_raw，返回张鑫要求标准job_list
    严格规范：
    - key大小写完全匹配
    - 空值全部为""，禁止None
    - salary拼接成 "8‑20k"格式
    - job_type固定为"全职"
    - welfare、skill 使用英文逗号分隔
    """
    conn = None
    cursor = None
    job_list = []
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"],
            charset="utf8mb4"
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM job_raw;"
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            s_min = row.get("salary_min")
            s_max = row.get("salary_max")
            if s_min is not None and s_max is not None:
                salary_str = f"{s_min}‑{s_max}k"
            else:
                salary_str = ""

            item = {
                "job_name": row.get("job_name", "") or "",
                "company_name": row.get("company_name", "") or "",
                "salary": salary_str,
                "city": row.get("city", "") or "",
                "education": row.get("education", "") or "",
                "experience": row.get("experience", "") or "",
                "job_type": "全职",
                "welfare": row.get("welfare", "") or "",
                "skill": row.get("skill_tags", "") or ""
            }
            job_list.append(item)
        logger.info(f"✅生成标准job_list，共 {len(job_list)} 条")
        return job_list
    except Exception as e:
        logger.error(f"读取mysql失败：{e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    # 1.建表
    create_job_raw_table()
    # 2.把csv导入mysql
    insert_csv_to_mysql()
    # 3.获取标准job_list
    job_list = get_job_list_from_job_raw()

    # 打印第一条样例，可以直接复制发给队友测试
    if len(job_list) > 0:
        print("\n=====样例job_list第一条（发给队友测试）=====")
        import pprint
        pprint.pprint(job_list[0])

    # ==========对接队友调用示例==========
    # from build_neo4j_kg import build_graph
    # build_graph(job_list)
