import pandas as pd
import random
import os
import pymysql
from config import MYSQL_CONFIG
from logger_util import logger

if not os.path.exists("./data"):
    os.makedirs("./data")

job_list_pool = ["数据分析师","数据开发工程师","算法工程师","AI大模型工程师","机器学习工程师","BI工程师"]
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

rows = []
for _ in range(250):
    job_name = random.choice(job_list_pool)
    company_name = random.choice(company_list)
    city = random.choice(city_list)
    salary_min = random.randint(8,22)
    salary_max = salary_min + random.randint(3,12)
    exp = random.choice(exp_list)
    edu = random.choice(edu_list)
    skill = random.choice(skill_list)
    ind = random.choice(industry_list)

    rows.append({
        "job_name": job_name,
        "company_name": company_name,
        "city": city,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "experience": exp,
        "education": edu,
        "skill_tags": skill,
        "industry": ind
    })

df = pd.DataFrame(rows)
csv_path = "./data/ai_ds_jobs.csv"
df.to_csv(csv_path, encoding="utf‑8‑sig", index=False)
logger.info(f"数据集生成完毕，路径 {csv_path}，共 {len(df)} 条")


def insert_csv_to_ai_ds_jobs():
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
        INSERT INTO ai_ds_jobs(job_name,company_name,salary_min,salary_max,city,education,experience,skill_tags,industry)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
                row["industry"]
            ))
        cursor.executemany(insert_sql, data_list)
        conn.commit()
        logger.info(f"成功插入 {len(data_list)} 条模拟数据到 ai_ds_jobs")
    except Exception as e:
        logger.error(f"插入失败：{e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_job_list_from_ai_ds_jobs():
    
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
        sql = "SELECT * FROM ai_ds_jobs;"
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
                "skill": row.get("skill_tags", "") or ""
            }
            job_list.append(item)
        logger.info(f"生成标准job_list，共 {len(job_list)} 条")
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
    insert_csv_to_ai_ds_jobs()
    job_list = get_job_list_from_ai_ds_jobs()

    if len(job_list) > 0:
        print("\n=====样例job_list第一条）=====")
        import pprint
        pprint.pprint(job_list[0])

   