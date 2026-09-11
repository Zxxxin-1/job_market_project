
from flask import Flask, jsonify, render_template, request
from logger_util import logger

app = Flask(__name__)


USE_REAL_ANALYSIS = True

if USE_REAL_ANALYSIS:
    from analysis import (
        stat_city_dist,
        stat_salary_by_city,
        stat_skill_hot,
        stat_salary_range,
    )


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


if __name__ == "__main__":
    logger.info("==== Flask 可视化后端启动 ====")
    app.run(host="127.0.0.1", port=5000, debug=True)