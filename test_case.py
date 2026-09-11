# test_case.py
# 陈智鸿：简易测试脚本
# 对 analysis.py 的 4 个统计函数做基础校验

from analysis import (
    stat_city_dist,
    stat_salary_by_city,
    stat_skill_hot,
    stat_salary_range
)


def test_city_dist():
    data = stat_city_dist()
    assert isinstance(data, list), "stat_city_dist 返回不是 list"
    assert len(data) > 0, "stat_city_dist 返回为空"
    for item in data:
        assert "city" in item, "缺少 city 字段"
        assert "job_count" in item, "缺少 job_count 字段"
        assert isinstance(item["city"], str), "city 不是 str"
        assert isinstance(item["job_count"], int), "job_count 不是 int"
    print("✅ test_city_dist 通过")


def test_salary_by_city():
    data = stat_salary_by_city()
    assert isinstance(data, list), "stat_salary_by_city 返回不是 list"
    assert len(data) > 0, "stat_salary_by_city 返回为空"
    for item in data:
        assert "city" in item, "缺少 city 字段"
        assert "avg_salary" in item, "缺少 avg_salary 字段"
        assert isinstance(item["city"], str), "city 不是 str"
        assert isinstance(item["avg_salary"], float), "avg_salary 不是 float"
    print("✅ test_salary_by_city 通过")


def test_skill_hot():
    data = stat_skill_hot()
    assert isinstance(data, list), "stat_skill_hot 返回不是 list"
    assert len(data) > 0, "stat_skill_hot 返回为空"
    for item in data:
        assert "skill" in item, "缺少 skill 字段"
        assert "count" in item, "缺少 count 字段"
        assert isinstance(item["skill"], str), "skill 不是 str"
        assert isinstance(item["count"], int), "count 不是 int"
    print("✅ test_skill_hot 通过")


def test_salary_range():
    data = stat_salary_range()
    assert isinstance(data, list), "stat_salary_range 返回不是 list"
    assert len(data) > 0, "stat_salary_range 返回为空"
    for item in data:
        assert "salary_range" in item, "缺少 salary_range 字段"
        assert "count" in item, "缺少 count 字段"
        assert isinstance(item["salary_range"], str), "salary_range 不是 str"
        assert isinstance(item["count"], int), "count 不是 int"
    print("✅ test_salary_range 通过")


if __name__ == "__main__":
    test_city_dist()
    test_salary_by_city()
    test_skill_hot()
    test_salary_range()
    print("\n🎉 全部测试通过")