"""Download compartilhado dos arquivos brutos da ANP.

Todos os estudos baixam com as mesmas regras:

- arquivo que já existe com tamanho > 0 é pulado (use ``force`` para rebaixar);
- até ``retries`` tentativas com backoff exponencial;
- escrita atômica (``.part`` → renomeia), sem arquivo pela metade em caso de erro;
- manifesto ``data/raw/{slug}/_manifest.json`` com URL, tamanho, sha256,
  ``Last-Modified`` e data do download de cada arquivo.

Estudos simples declaram os arquivos em ``config/monorepo.yaml`` (bloco
``download``); estudos com regras próprias (PMQC, preços, poço) montam a lista
em Python e chamam ``download_all``.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (anp-fuel-analytics; research)"
MANIFEST_NAME = "_manifest.json"


@dataclass(frozen=True)
class Remote:
    """Um arquivo do portal e onde ele fica em ``data/raw/{slug}/``."""

    url: str
    dest: str
    extract_to: str | None = None  # pasta (relativa ao raw) para extrair ZIPs
    extract_marker: bool = False  # True = extrai só uma vez (cria .extracted)


def remotes_from_config(block: dict) -> list[Remote]:
    """Converte o bloco ``download`` do YAML em uma lista de ``Remote``.

    Cada item de ``files`` pode ser:
      - ``"nome.csv"`` → ``{base}/nome.csv`` salvo como ``nome.csv``;
      - ``{src: "a/b.csv", dest: "sub/b.csv"}`` → caminho relativo à ``base``;
      - ``{url: "https://...", dest: "x.xlsx"}`` → URL completa;
      - ``extract_to`` / ``extract_marker`` opcionais para ZIPs.
    """
    base = block.get("base", "").rstrip("/")
    out: list[Remote] = []
    for item in block.get("files", []):
        if isinstance(item, str):
            item = {"src": item}
        if "url" in item:
            url = item["url"]
            default_dest = url.rsplit("/", 1)[-1]
        else:
            if not base:
                raise ValueError(f"Item sem 'url' e bloco sem 'base': {item}")
            url = f"{base}/{item['src']}"
            default_dest = item["src"].rsplit("/", 1)[-1]
        out.append(
            Remote(
                url=url,
                dest=item.get("dest", default_dest),
                extract_to=item.get("extract_to"),
                extract_marker=bool(item.get("extract_marker", False)),
            )
        )
    return out


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def fetch(
    url: str,
    dest: Path,
    *,
    timeout: int = 180,
    retries: int = 3,
    backoff: float = 2.0,
    user_agent: str = USER_AGENT,
) -> dict:
    """Baixa ``url`` para ``dest`` e devolve os cabeçalhos úteis para o manifesto."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp, tmp.open("wb") as out:
                while block := resp.read(1 << 20):
                    out.write(block)
                headers = {
                    "last_modified": resp.headers.get("Last-Modified"),
                    "etag": resp.headers.get("ETag"),
                }
            tmp.replace(dest)
            return headers
        except urllib.error.HTTPError as e:
            last_error = e
            if 400 <= e.code < 500 and e.code != 429:
                break  # 404/403 não melhoram com retry
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last_error = e
        if attempt < retries:
            time.sleep(backoff ** attempt)
    if tmp.exists():
        tmp.unlink()
    raise RuntimeError(f"{url}: {last_error}") from last_error


def extract_zip(zip_path: Path, dest_dir: Path, *, marker: bool = False) -> bool:
    """Extrai ``zip_path`` em ``dest_dir``. Com ``marker``, extrai uma única vez."""
    flag = dest_dir / ".extracted"
    if marker and flag.exists():
        return False
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest_dir)
    if marker:
        flag.write_text("ok\n", encoding="utf-8")
    return True


class Manifest:
    """Registro do que foi baixado em ``data/raw/{slug}/_manifest.json``."""

    def __init__(self, raw_root: Path) -> None:
        self.path = raw_root / MANIFEST_NAME
        self.entries: dict[str, dict] = {}
        if self.path.exists():
            self.entries = json.loads(self.path.read_text(encoding="utf-8")).get("files", {})

    def record(self, rel: str, url: str, file: Path, headers: dict | None = None) -> None:
        stat = file.stat()
        old = self.entries.get(rel, {})
        same_file = old.get("bytes") == stat.st_size and old.get("mtime") == int(stat.st_mtime)
        entry = {
            "url": url,
            "bytes": stat.st_size,
            "mtime": int(stat.st_mtime),
            "sha256": old["sha256"] if same_file and "sha256" in old else sha256(file),
            "downloaded_at": _now() if headers is not None else old.get("downloaded_at") or _iso(stat.st_mtime),
        }
        if headers:
            entry.update({k: v for k, v in headers.items() if v})
        elif same_file:
            entry.update({k: old[k] for k in ("last_modified", "etag") if k in old})
        self.entries[rel] = entry

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"generated_at": _now(), "files": dict(sorted(self.entries.items()))}
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def download_all(
    raw_root: Path,
    remotes: list[Remote],
    *,
    timeout: int = 180,
    force: bool = False,
    log_root: Path | None = None,
) -> int:
    """Baixa a lista, atualiza o manifesto e devolve o número de falhas."""
    manifest = Manifest(raw_root)
    ok = skip = fail = 0
    show = (lambda p: p.relative_to(log_root)) if log_root else (lambda p: p)
    for r in remotes:
        dest = raw_root / r.dest
        headers = None
        if dest.exists() and dest.stat().st_size > 0 and not force:
            skip += 1
        else:
            try:
                print(f"get  {show(dest)}")
                headers = fetch(r.url, dest, timeout=timeout)
                ok += 1
            except Exception as e:  # noqa: BLE001 — registra e segue para o próximo arquivo
                print(f"FAIL {r.dest}: {e}")
                fail += 1
                continue
        manifest.record(r.dest, r.url, dest, headers)
        if r.extract_to is not None and dest.suffix.lower() == ".zip":
            target = raw_root / r.extract_to
            try:
                if extract_zip(dest, target, marker=r.extract_marker):
                    print(f"unzip {r.dest} -> {show(target)}")
            except zipfile.BadZipFile as e:
                print(f"FAIL unzip {r.dest}: {e}")
                fail += 1
    manifest.save()
    print(f"\n{ok} baixados, {skip} já existiam, {fail} falhas -> {show(raw_root)}")
    return fail


def check_remotes(remotes: list[Remote], *, timeout: int = 30) -> list[tuple[str, str]]:
    """Testa cada URL pedindo só o 1º byte (o portal nem sempre aceita HEAD).

    Devolve [(url, erro)] dos que falharam.
    """
    broken: list[tuple[str, str]] = []
    for r in remotes:
        req = urllib.request.Request(r.url, headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                resp.read(1)
        except Exception as e:  # noqa: BLE001
            broken.append((r.url, str(e)))
    return broken


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).replace(microsecond=0).isoformat()


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main_for(slug: str, remotes: list[Remote], *, timeout: int = 180, argv: list[str] | None = None) -> None:
    """CLI comum: ``--force`` rebaixa tudo, ``--check`` só testa se as URLs respondem."""
    import argparse
    import sys

    from core.config import REPO_ROOT, study_paths

    parser = argparse.ArgumentParser(description=f"Download raw de {slug}")
    parser.add_argument("--force", action="store_true", help="rebaixa arquivos já existentes")
    parser.add_argument("--check", action="store_true", help="só verifica se as URLs respondem")
    args, _ = parser.parse_known_args(argv)

    if args.check:
        broken = check_remotes(remotes)
        for url, err in broken:
            print(f"QUEBRADO {url}: {err}")
        print(f"{len(remotes) - len(broken)}/{len(remotes)} URLs ok ({slug})")
        sys.exit(1 if broken else 0)

    root = study_paths(slug)["raw"]
    failures = download_all(root, remotes, timeout=timeout, force=args.force, log_root=REPO_ROOT)
    sys.exit(1 if failures else 0)
