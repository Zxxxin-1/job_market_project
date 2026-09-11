import os
import traceback
import pandas as pd
import pymysql
from config import MYSQL_CONFIG
from logger_util import logger


def read_csv_auto_encode(file_path):
    df = None
    try:
        df = pd.read_csv(file_path, encoding="utf‑8‑sig")
        logger.info(f"{file_path} 使用 utf‑8‑sig 读取成功")
    except Exception:
        try:
            df = pd.read_csv(file_path, encoding="gbk")
            logger.info(f"{file_path} 使用 gbk 读取成功")
        except Exception as err:
            logger.error(f"读取csv失败！{str(err)}")
            raise err
    return df


def clean_dataframe(df):
    total_raw = len(df)
    logger.info(f"原始csv读取行数：{total_raw}")

    need_cols = [
        "job_name", "company_name", "city", "salary_min", "salary_max",
        "experience", "education", "skill_tags", "industry"
    ]
    exist_cols = [c for c in need_cols if c in df.columns]
    df = df[exist_cols].copy()

    for col in ["job_name", "company_name", "city", "experience", "education", "skill_tags", "industry"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

    for col in ["salary_min", "salary_max"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.drop_duplicates(subset=["job_name", "company_name", "city"], keep="first", inplace=True)
    after_dup = len(df)
    drop_dup = total_raw - after_dup
    logger.info(f"去重丢弃 {drop_dup} 条重复记录")

    df = df[~((df["job_name"] == "") | (df["company_name"] == ""))]
    after_clean = len(df)
    drop_empty = after_dup - after_clean
    logger.info(f"丢弃核心字段为空脏数据 {drop_empty} 条")
    return df


def batch_insert_mysql(df):
    conn = None
    cursor = None
    insert_sql = """
    INSERT INTO `ai_ds_jobs`
    (job_name, company_name, city, salary_min, salary_max, experience, education, skill_tags, industry)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
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
        insert_list = []
        for _, row in df.iterrows():
            item = (
                row["job_name"],
                row["company_name"],
                row["city"],
                row["salary_min"] if pd.notna(row["salary_min"]) else None,
                row["salary_max"] if pd.notna(row["salary_max"]) else None,
                row["experience"],
                row["education"],
                row["skill_tags"],
                row["industry"]
            )
            insert_list.append(item)

        if len(insert_list) > 0:
            cursor.executemany(insert_sql, insert_list)
            conn.commit()
            logger.info(f"批量入库成功，共写入 {cursor.rowcount} 条岗位数据")
        else:
            logger.warning("没有可写入的数据！")

    except Exception as e:
        logger.error(f"批量入库异常：{str(e)}")
        logger.error(traceback.format_exc())
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def main():
    csv_path = os.path.join("data", "ai_ds_jobs.csv")
    if not os.path.exists(csv_path):
        logger.error(f"找不到数据集文件 {csv_path}！请把csv放到data文件夹下")
        return

    logger.info("====spider_data.py开始执行，读取数据集====")
    df_raw = read_csv_auto_encode(csv_path)
    df_clean = clean_dataframe(df_raw)
    batch_insert_mysql(df_clean)
    logger.info("====spider_data.py执行完毕====")


if __name__ == "__main__":
    main()
