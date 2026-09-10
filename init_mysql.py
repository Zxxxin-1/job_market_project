import pymysql
import traceback
from config import MYSQL_CONFIG
from logger_util import logger


def init_database_and_table():
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            charset="utf8mb4"
        )
        cursor = conn.cursor()
        create_db_sql = "CREATE DATABASE IF NOT EXISTS `job_market` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
        cursor.execute(create_db_sql)
        logger.info("数据库 job_market 创建/校验完成")

        cursor.execute("USE `job_market`;")

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS `ai_ds_jobs` (
            `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
            `job_name` VARCHAR(255) COMMENT '岗位名称',
            `company_name` VARCHAR(255) COMMENT '企业名称',
            `city` VARCHAR(100) COMMENT '城市',
            `salary_min` INT NULL COMMENT '最低薪资',
            `salary_max` INT NULL COMMENT '最高薪资',
            `experience` VARCHAR(100) COMMENT '工作经验',
            `education` VARCHAR(100) COMMENT '学历',
            `skill_tags` TEXT COMMENT '技能标签，逗号分隔',
            `industry` VARCHAR(255) COMMENT '所属行业'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='岗位数据表';
        """
        cursor.execute(create_table_sql)
        conn.commit()
        logger.info("数据表 ai_ds_jobs 创建/校验完成！")

    except Exception as e:
        logger.error(f"初始化数据库失败：{str(e)}")
        logger.error(traceback.format_exc())
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    logger.info("====开始执行MySQL初始化脚本 init_mysql.py====")
    init_database_and_table()
    logger.info("====init_mysql.py执行结束====")
