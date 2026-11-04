import http.server
import io
import json
import threading
import zipfile
from functools import partial

import pytest

from core.download import Remote, download_all, remotes_from_config


@pytest.fixture
def server(tmp_path):
    root = tmp_path / "portal"
    root.mkdir()
    (root / "a.csv").write_text("x;y\n1;2\n", encoding="utf-8")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("dentro.csv", "c\n3\n")
    (root / "b.zip").write_bytes(buf.getvalue())
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    handler.log_message = lambda *a, **k: None
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def test_download_manifest_skip_and_extract(server, tmp_path):
    raw = tmp_path / "raw"
    remotes = [
        Remote(f"{server}/a.csv", "sub/a.csv"),
        Remote(f"{server}/b.zip", "b.zip", extract_to="b", extract_marker=True),
    ]
    assert download_all(raw, remotes) == 0
    assert (raw / "sub/a.csv").read_text(encoding="utf-8").startswith("x;y")
    assert (raw / "b/dentro.csv").exists()
    assert (raw / "b/.extracted").exists()

    manifest = json.loads((raw / "_manifest.json").read_text(encoding="utf-8"))["files"]
    assert set(manifest) == {"sub/a.csv", "b.zip"}
    assert len(manifest["sub/a.csv"]["sha256"]) == 64
    assert manifest["sub/a.csv"]["url"].endswith("/a.csv")

    # segunda execução: nada é baixado de novo e o manifesto continua igual
    first = manifest["sub/a.csv"]["downloaded_at"]
    assert download_all(raw, remotes) == 0
    again = json.loads((raw / "_manifest.json").read_text(encoding="utf-8"))["files"]
    assert again["sub/a.csv"]["downloaded_at"] == first


def test_download_failure_is_counted_and_leaves_no_partial(server, tmp_path):
    raw = tmp_path / "raw"
    failures = download_all(raw, [Remote(f"{server}/nao-existe.csv", "x.csv")])
    assert failures == 1
    assert not (raw / "x.csv").exists()
    assert not list(raw.glob("*.part"))


def test_remotes_from_config_forms():
    block = {
        "base": "https://exemplo/base/",
        "files": [
            "a.pdf",
            {"src": "dir/b.csv", "dest": "sub/b.csv"},
            {"url": "https://outro/c.xlsx", "dest": "c.xlsx"},
            {"src": "d.zip", "extract_to": "d", "extract_marker": True},
        ],
    }
    r = remotes_from_config(block)
    assert [(x.url, x.dest) for x in r] == [
        ("https://exemplo/base/a.pdf", "a.pdf"),
        ("https://exemplo/base/dir/b.csv", "sub/b.csv"),
        ("https://outro/c.xlsx", "c.xlsx"),
        ("https://exemplo/base/d.zip", "d.zip"),
    ]
    assert r[3].extract_to == "d" and r[3].extract_marker
