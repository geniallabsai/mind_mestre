# -*- coding: utf-8 -*-
"""Percorre o material da pessoa — notas, entrevistas, ideias, conquistas.
Extrai a matéria-prima: arquivos, seções, frases e onde cada frase foi dita
(arquivo:linha). Tudo o que os agentes afirmam depois aponta para cá."""
import os
import re

EXT_OK = {".md", ".txt", ".markdown", ".rst", ".text"}
DIRS_IGNORE = {".git", "__pycache__", "node_modules", "saida", ".obsidian", ".idea"}


def normalizar(texto):
    """minúsculas + sem acentos — o casamento de sinais fica à prova de til."""
    t = (texto or "").lower()
    for a, b in (("á", "a"), ("à", "a"), ("ã", "a"), ("â", "a"),
                 ("é", "e"), ("ê", "e"), ("í", "i"), ("õ", "o"), ("ó", "o"),
                 ("ô", "o"), ("ú", "u"), ("ç", "c")):
        t = t.replace(a, b)
    return t


def listar_arquivos(alvo):
    alvo = os.path.abspath(alvo)
    if os.path.isfile(alvo):
        return [alvo]
    caminhos = []
    for raiz, dirs, fs in os.walk(alvo):
        dirs[:] = sorted(d for d in dirs if d not in DIRS_IGNORE and not d.startswith("."))
        for f in sorted(fs):
            p = os.path.join(raiz, f)
            if f.lower().startswith("readme"):
                continue  # readme documenta a pasta; o conteúdo é outra coisa
            if os.path.splitext(f)[1].lower() in EXT_OK:
                caminhos.append(p)
    return caminhos


def ler_texto(caminho):
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(caminho, encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, OSError):
            continue
    return ""


def extrair_secoes(texto, arquivo):
    secoes = []
    for i, l in enumerate(texto.splitlines(), 1):
        m = re.match(r"^#{1,6}\s+(.+?)\s*$", l)
        if m:
            secoes.append({"titulo": m.group(1), "arquivo": arquivo, "linha": i})
    return secoes


def frases(texto):
    bruto = re.sub(r"\s+", " ", texto)
    partes = re.split(r"(?<=[.!?…])\s+", bruto)
    return [p.strip() for p in partes if 20 <= len(p.strip()) <= 400]


def linha_de(texto, trecho):
    """Linha onde o trecho aparece — janelas decrescentes: o trecho pode nascer
    no meio de uma linha ou atravessar quebra de linha."""
    base = normalizar(re.sub(r"\s+", " ", trecho.strip()))
    if not base:
        return None
    norm_linhas = [normalizar(l) for l in texto.splitlines()]
    for tam in (48, 32, 20, 12):
        alvo = base[:tam]
        if len(alvo) >= 8:
            for i, nl in enumerate(norm_linhas, 1):
                if alvo in nl:
                    return i
    for w in base.split():
        if len(w) >= 5:
            for i, nl in enumerate(norm_linhas, 1):
                if w in nl:
                    return i
            break
    return None


def trechos_ao_redor(texto, pos, largura=110):
    ini = max(0, pos - largura // 2)
    fim = min(len(texto), pos + largura // 2)
    t = texto[ini:fim].replace("\n", " ").strip()
    return re.sub(r"\s+", " ", t)[:160]
