import pytest

from core.run_sql import _split_statements, render_sql


def test_render_sql_replaces_and_fails_on_missing():
    assert render_sql("select '{{A}}'", {"A": "x"}) == "select 'x'"
    with pytest.raises(KeyError):
        render_sql("select '{{B}}'", {"A": "x"})


def test_split_statements():
    parts = _split_statements("select 1;\nselect\n  2;\n")
    assert [p.strip() for p in parts if p.strip()] == ["select 1;", "select\n  2;"]
