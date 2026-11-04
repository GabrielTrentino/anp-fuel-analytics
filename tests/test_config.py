"""Coerência do config/monorepo.yaml com scripts, SQL e estudos."""
import re

import pytest

from conftest import REPO_ROOT
from core.config import load_config
from core.download import remotes_from_config
from run import sql_placeholders, sql_vars, step_outputs

CFG = load_config()
STUDIES = CFG["studies"]
ALL_OUTPUTS = {o for s in STUDIES.values() for step in s["pipeline"] for o in step_outputs(step)}


def _steps():
    for slug, study in STUDIES.items():
        for step in study["pipeline"]:
            yield pytest.param(slug, study, step, id=f"{slug}/{step['step']}")


@pytest.mark.parametrize("slug,study,step", list(_steps()))
def test_step_is_runnable(slug, study, step):
    engine = step["engine"]
    assert engine in {"download", "python", "sql"}
    if engine == "download":
        assert study.get("download", {}).get("files"), "engine download exige bloco download.files"
        return
    script = REPO_ROOT / step["script"]
    assert script.exists(), f"script inexistente: {step['script']}"
    if engine == "sql":
        assert step_outputs(step), "etapa SQL precisa declarar outputs"
        missing = sql_placeholders(script) - set(sql_vars(study, step))
        assert not missing, f"variáveis sem valor em {step['script']}: {sorted(missing)}"


@pytest.mark.parametrize("slug", STUDIES)
def test_step_names_are_unique(slug):
    names = [s["step"] for s in STUDIES[slug]["pipeline"]]
    assert len(names) == len(set(names))


@pytest.mark.parametrize("slug", [s for s in STUDIES if "download" in STUDIES[s]])
def test_download_block(slug):
    remotes = remotes_from_config(STUDIES[slug]["download"])
    assert remotes
    dests = [r.dest for r in remotes]
    assert len(dests) == len(set(dests)), "dois arquivos com o mesmo destino"
    for r in remotes:
        assert r.url.startswith("https://www.gov.br/anp/"), r.url
        assert not r.dest.startswith(("/", "..")), r.dest


@pytest.mark.parametrize("slug", STUDIES)
def test_quality_targets_declared_outputs(slug):
    for item in STUDIES[slug].get("quality", []):
        assert item["table"] in ALL_OUTPUTS, f"{item['table']} não é saída de nenhuma etapa"


def test_every_trusted_output_has_quality_check():
    checked = {i["table"] for s in STUDIES.values() for i in s.get("quality", [])}
    trusted = {o for o in ALL_OUTPUTS if o.startswith("data/trusted/") and "/uf/" not in o}
    assert trusted - checked == set()


PARQUET_REF = re.compile(r"""["'/]((?:data/)?(?:trusted|refined)/[\w./-]+?\.parquet)""")


def _references():
    for path in sorted((REPO_ROOT / "estudos").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        # TRUSTED / "slug" / "arquivo.parquet"  ->  data/trusted/slug/arquivo.parquet
        for layer, slug, name in re.findall(r'(TRUSTED|REFINED) / "([\w-]+)" / "([\w.-]+\.parquet)"', text):
            yield path, f"data/{layer.lower()}/{slug}/{name}"
        for ref in PARQUET_REF.findall(text):
            yield path, ref if ref.startswith("data/") else f"data/{ref}"


@pytest.mark.parametrize("path,ref", list(_references()), ids=lambda v: str(v)[-60:])
def test_study_scripts_read_declared_outputs(path, ref):
    assert ref in ALL_OUTPUTS, f"{path.relative_to(REPO_ROOT)} lê {ref}, que nenhuma etapa gera"
