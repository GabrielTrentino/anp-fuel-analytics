"""Probe ANP portal for cadastro revendas combustiveis download links."""
from __future__ import annotations

import re
import urllib.request

URL = (
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/"
    "dados-cadastrais-dos-revendedores-varejistas-de-combustiveis-automotivos"
)
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (anp-fuel-analytics)"})
html = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", errors="replace")
links = sorted(set(re.findall(r'href="([^"]*(?:csv|zip|pdf|xlsx)[^"]*)"', html, re.I)))
for link in links:
    print(link)
print("--- total", len(links))
