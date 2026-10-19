import duckdb

from core.quality import has_errors, run_checks


def _table(tmp_path):
    path = tmp_path / "t.parquet"
    duckdb.sql(
        "COPY (SELECT * FROM (VALUES (1, 'SP', 10.0), (2, 'RJ', 20.0), (2, 'RJ', 20.0), (3, 'XX', NULL)) "
        f"t(id, uf, v)) TO '{path.as_posix()}' (FORMAT PARQUET)"
    )
    return "t.parquet"


def test_rules_detect_problems(tmp_path):
    item = {
        "table": _table(tmp_path),
        "min_rows": 10,
        "not_null": ["v"],
        "unique": ["id"],
        "no_duplicate_rows": True,
        "accepted_values": {"uf": ["SP", "RJ"]},
        "range": {"v": {"min": 0, "max": 15}},
    }
    res = {r.rule: r for r in run_checks(item, tmp_path)}
    assert not res["min_rows"].passed
    assert res["not_null"].failing == 1
    assert res["unique"].failing == 1
    assert res["no_duplicate_rows"].failing == 1
    assert res["accepted_values"].failing == 1
    assert res["range"].failing == 2
    assert has_errors(list(res.values()))


def test_warn_does_not_fail_and_good_table_passes(tmp_path):
    table = _table(tmp_path)
    warn = run_checks({"table": table, "unique": {"columns": ["id"], "severity": "warn", "note": "fonte"}}, tmp_path)
    assert warn[0].status == "aviso" and not has_errors(warn)
    ok = run_checks({"table": table, "min_rows": 4, "not_null": ["id", "uf"]}, tmp_path)
    assert all(r.passed for r in ok)


def test_missing_table_and_unknown_rule(tmp_path):
    assert run_checks({"table": "nao/existe.parquet"}, tmp_path)[0].rule == "exists"
    res = run_checks({"table": _table(tmp_path), "uniq": ["id"]}, tmp_path)
    assert res[-1].rule == "config" and has_errors(res)
