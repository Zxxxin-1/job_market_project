import pymysql
import pandas as pd
from config import MYSQL_CONFIG
from logger_util import logger


def load_jobs_df():
    
    conn = None
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"],
            charset="utf8mb4"
        )
        sql = "SELECT * FROM ai_ds_jobs;"
        df = pd.read_sql(sql, conn)
        logger.info(f"analysis.py 读取 MySQL 成功，共 {len(df)} 条岗位数据")
        return df
    except Exception as e:
        logger.error(f"analysis.py 读取 MySQL 失败：{str(e)}", exc_info=True)
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()


def stat_city_dist():
    
    try:
        df = load_jobs_df()
        if df.empty:
            logger.warning("stat_city_dist: 数据为空")
            return []

        result_df = df.groupby("city").size().reset_index(name="job_count")
        result_df = result_df.sort_values(by="job_count", ascending=False)

        result = []
        for _, row in result_df.iterrows():
            result.append({
                "city": str(row["city"]),
                "job_count": int(row["job_count"])
            })
        logger.info(f"stat_city_dist 统计完成，城市数：{len(result)}")
        return result
    except Exception as e:
        logger.error(f"stat_city_dist 统计失败：{str(e)}", exc_info=True)
        return []


def stat_salary_by_city():
    
    try:
        df = load_jobs_df()
        if df.empty:
            logger.warning("stat_salary_by_city: 数据为空")
            return []

        # 处理空值
        df = df.dropna(subset=["salary_min", "salary_max"]).copy()
        if df.empty:
            logger.warning("stat_salary_by_city: 薪资字段全部为空")
            return []

        df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
        df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
        df = df.dropna(subset=["salary_min", "salary_max"])

        df["avg_salary"] = (df["salary_min"] + df["salary_max"]) / 2

        result_df = df.groupby("city")["avg_salary"].mean().reset_index()
        result_df["avg_salary"] = result_df["avg_salary"].round(2)
        result_df = result_df.sort_values(by="avg_salary", ascending=False)

        result = []
        for _, row in result_df.iterrows():
            result.append({
                "city": str(row["city"]),
                "avg_salary": float(row["avg_salary"])
            })
        logger.info(f"stat_salary_by_city 统计完成，城市数：{len(result)}")
        return result
    except Exception as e:
        logger.error(f"stat_salary_by_city 统计失败：{str(e)}", exc_info=True)
        return []


def stat_skill_hot():
    
    try:
        df = load_jobs_df()
        if df.empty:
            logger.warning("stat_skill_hot: 数据为空")
            return []

        skill_counter = {}
        for tags in df["skill_tags"].dropna():
            tags_str = str(tags).strip()
            if not tags_str:
                continue
            for skill in tags_str.split(","):
                skill = skill.strip()
                if skill:
                    skill_counter[skill] = skill_counter.get(skill, 0) + 1

        sorted_skills = sorted(skill_counter.items(), key=lambda x: x[1], reverse=True)

        result = []
        for skill, count in sorted_skills:
            result.append({
                "skill": str(skill),
                "count": int(count)
            })
        logger.info(f"stat_skill_hot 统计完成，技能数：{len(result)}")
        return result
    except Exception as e:
        logger.error(f"stat_skill_hot 统计失败：{str(e)}", exc_info=True)
        return []


def stat_salary_range():
    
    try:
        df = load_jobs_df()
        if df.empty:
            logger.warning("stat_salary_range: 数据为空")
            return []

        df = df.dropna(subset=["salary_min", "salary_max"]).copy()
        if df.empty:
            logger.warning("stat_salary_range: 薪资字段全部为空")
            return []

        df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
        df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
        df = df.dropna(subset=["salary_min", "salary_max"])

        df["avg_salary"] = (df["salary_min"] + df["salary_max"]) / 2

        def salary_range_label(avg):
            if avg < 10:
                return "0-10k"
            elif avg < 15:
                return "10-15k"
            elif avg < 20:
                return "15-20k"
            elif avg < 25:
                return "20-25k"
            else:
                return "25k以上"

        df["salary_range"] = df["avg_salary"].apply(salary_range_label)

        range_order = ["0-10k", "10-15k", "15-20k", "20-25k", "25k以上"]
        result_df = df.groupby("salary_range").size().reset_index(name="count")

        result = []
        for r in range_order:
            matched = result_df[result_df["salary_range"] == r]
            if not matched.empty:
                count = int(matched.iloc[0]["count"])
            else:
                count = 0
            result.append({
                "salary_range": r,
                "count": count
            })
        logger.info(f"stat_salary_range 统计完成，区间数：{len(result)}")
        return result
    except Exception as e:
        logger.error(f"stat_salary_range 统计失败：{str(e)}", exc_info=True)
        return []


def export_sample_json():
    
    import os
    import json

    if not os.path.exists("temp_output"):
        os.makedirs("temp_output")

    data = {
        "city_dist": stat_city_dist(),
        "salary_by_city": stat_salary_by_city(),
        "skill_hot": stat_skill_hot(),
        "salary_range": stat_salary_range()
    }

    output_path = os.path.join("temp_output", "sample_stats.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"样例 JSON 已导出：{output_path}")
    print(f"样例 JSON 已导出：{output_path}")


if __name__ == "__main__":
    logger.info("==== analysis.py 开始执行 ====")

    print("\n===== stat_city_dist =====")
    for item in stat_city_dist():
        print(item)

    print("\n===== stat_salary_by_city =====")
    for item in stat_salary_by_city():
        print(item)

    print("\n===== stat_skill_hot =====")
    for item in stat_skill_hot():
        print(item)

    print("\n===== stat_salary_range =====")
    for item in stat_salary_range():
        print(item)

    export_sample_json()

    logger.info("==== analysis.py 执行结束 ====")