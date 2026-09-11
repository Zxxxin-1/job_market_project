from flask import Flask, jsonify, render_template, request
from logger_util import logger
from neo4j import GraphDatabase, basic_auth
from config import NEO4J_CONFIG
import webbrowser
import threading
import time
import random
app = Flask(__name__)
USE_REAL_ANALYSIS = True
# 导入数据分析函数
if USE_REAL_ANALYSIS:
    from analysis import (
        stat_city_dist,
        stat_salary_by_city,
        stat_skill_hot,
        stat_salary_range,
    )
# Neo4j连接配置
NEO4J_URI = NEO4J_CONFIG["uri"]
NEO4J_USER = NEO4J_CONFIG["user"]
NEO4J_PWD = NEO4J_CONFIG["password"]
def normalize_data(data):
    """把 numpy.int64/float64 等转成原生 Python 类型，Flask才能jsonify"""
    result = []
    for row in data:
        new_row = {}
        for k, v in row.items():
            if hasattr(v, "item"):
                v = v.item()
            new_row[k] = v
        result.append(new_row)
    return result
@app.before_request
def before_request_log():
    logger.info(f"[接口访问] {request.method} {request.path}")
@app.after_request
def after_request_log(response):
    logger.info(f"[接口响应] {request.path} {response.status_code}")
    return response
@app.route("/")
def index():
    return render_template("dashboard.html")
@app.route("/api/city_dist")
def api_city_dist():
    try:
        if USE_REAL_ANALYSIS:
            data = stat_city_dist()
        else:
            data = [
                {"city": "北京", "job_count": 40},
                {"city": "上海", "job_count": 35},
                {"city": "深圳", "job_count": 30},
                {"city": "杭州", "job_count": 25},
                {"city": "大连", "job_count": 20},
            ]
        return jsonify({"data": normalize_data(data)})
    except Exception as e:
        logger.error(f"city_dist 接口异常: {e}", exc_info=True)
        return jsonify({"data": [], "error": str(e)}), 500
@app.route("/api/salary_by_city")
def api_salary_by_city():
    try:
        if USE_REAL_ANALYSIS:
            data = stat_salary_by_city()
        else:
            data = [
                {"city": "北京", "avg_salary": 18000},
                {"city": "上海", "avg_salary": 17000},
                {"city": "深圳", "avg_salary": 16500},
                {"city": "杭州", "avg_salary": 15500},
                {"city": "大连", "avg_salary": 13000},
            ]
        return jsonify({"data": normalize_data(data)})
    except Exception as e:
        logger.error(f"salary_by_city 接口异常: {e}", exc_info=True)
        return jsonify({"data": [], "error": str(e)}), 500
@app.route("/api/skill_hot")
def api_skill_hot():
    try:
        if USE_REAL_ANALYSIS:
            data = stat_skill_hot()
        else:
            data = [
                {"skill": "Python", "count": 80},
                {"skill": "SQL", "count": 65},
                {"skill": "Pandas", "count": 45},
                {"skill": "Tensorflow", "count": 40},
                {"skill": "Pytorch", "count": 38},
                {"skill": "大模型", "count": 35},
                {"skill": "Hive", "count": 30},
                {"skill": "Spark", "count": 28},
            ]
        return jsonify({"data": normalize_data(data)})
    except Exception as e:
        logger.error(f"skill_hot 接口异常: {e}", exc_info=True)
        return jsonify({"data": [], "error": str(e)}), 500
@app.route("/api/salary_range")
def api_salary_range():
    try:
        if USE_REAL_ANALYSIS:
            data = stat_salary_range()
        else:
            data = [
                {"salary_range": "0-10k", "count": 10},
                {"salary_range": "10-15k", "count": 30},
                {"salary_range": "15-20k", "count": 45},
                {"salary_range": "20-30k", "count": 25},
                {"salary_range": "30k以上", "count": 8},
            ]
        return jsonify({"data": normalize_data(data)})
    except Exception as e:
        logger.error(f"salary_range 接口异常: {e}", exc_info=True)
        return jsonify({"data": [], "error": str(e)}), 500
# 知识图谱接口（重点：数据库保持完整，接口过滤小众岗位，前端只展示核心岗位相关节点）
@app.route("/api/kg_data")
def api_kg_data():
    driver = None
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PWD))
        with driver.session() as session:
            # 筛选目标岗位名称：算法工程师、数据分析师、BI工程师、数据开发工程师、机器学习工程师
            job_res = session.run("""
                MATCH (j:Job)
                WHERE j.job_name IN ["算法工程师", "数据分析师", "BI工程师", "数据开发工程师", "机器学习工程师"]
                RETURN id(j) AS job_id
            """)
            target_job_ids = set()
            for record in job_res:
                target_job_ids.add(record["job_id"])

            node_res = session.run("""
                MATCH (n)
                WHERE id(n) IN $jobid_list OR EXISTS{
                    MATCH (n)<--(j:Job) WHERE id(j) IN $jobid_list
                }
                RETURN id(n) AS node_id, labels(n) AS label, properties(n) AS props
            """, jobid_list=list(target_job_ids))

            all_nodes = []
            for record in node_res:
                neo4j_id = record["node_id"]
                label_list = record["label"]
                props = record["props"]
                label = label_list[0] if len(label_list) > 0 else "Unknown"
                name = ""
                if label == "Job":
                    name = props.get("job_name", "未知岗位")
                elif label == "Skill":
                    name = props.get("name", "未知技能")
                elif label == "Company":
                    name = props.get("name", "未知公司")
                elif label == "City":
                    name = props.get("name", "未知城市")
                all_nodes.append({
                    "neo_id": neo4j_id,
                    "name": name,
                    "label": label
                })

            max_front_node = 200
            if len(all_nodes) > max_front_node:
                all_nodes = random.sample(all_nodes, k=max_front_node)
            sample_neo_ids = set([item["neo_id"] for item in all_nodes])

            node_id_map = {}
            nodes = []
            for idx, node in enumerate(all_nodes):
                node_id_map[node["neo_id"]] = idx
                nodes.append({
                    "id": idx,
                    "name": node["name"],
                    "label": node["label"]
                })

            link_res = session.run("""
                MATCH (n)-[r]->(m)
                WHERE id(n) IN $id_list AND id(m) IN $id_list
                RETURN id(startNode(r)) AS source_id, id(endNode(r)) AS target_id, type(r) AS rel_name
            """, id_list=list(sample_neo_ids))
            links = []
            for record in link_res:
                source_id = record["source_id"]
                target_id = record["target_id"]
                rel_name = record["rel_name"]
                if source_id in node_id_map and target_id in node_id_map:
                    links.append({
                        "source": node_id_map[source_id],
                        "target": node_id_map[target_id],
                        "name": rel_name
                    })
            # 限制关系最多1000条
            if len(links) > 1000:
                links = random.sample(links, k=1000)
        logger.info(f"图谱接口【前端过滤核心岗位】读取成功：节点{len(nodes)}个，关系{len(links)}条（Neo4j数据库原始数据完整不变）")
        return jsonify({"nodes": nodes, "links": links})
    except Exception as e:
        logger.error(f"kg_data接口读取Neo4j异常: {e}", exc_info=True)
        return jsonify({"nodes": [], "links": []}), 500
    finally:
        if driver:
            driver.close()
def open_page():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:8080")
if __name__ == '__main__':
    logger.info("==== Flask 可视化后端启动 ====")
    threading.Timer(1.2, open_page).start()
    app.run(host="127.0.0.1", port=8080, debug=False)
