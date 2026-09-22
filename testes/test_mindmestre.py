#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Suíte do Mind Mestre — roda offline (MIND_SEM_IA=1)."""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
os.environ["MIND_SEM_IA"] = "1"

from mind_core import llm, mermaid, relatorios            # noqa: E402
from mind_core import leitura_pessoal                      # noqa: E402
from mind_core.arte import bloco                           # noqa: E402
from agentes import (Cartografo, Cetico, Conteudista, Convicto, Copista,  # noqa: E402
                     Detetive, Estrategista, GenioMarketing, Inquisidor,
                     Juiz, Posicionador)
from agentes.inquisidor import medir_nuance                # noqa: E402
from agentes.copista import CORPUS                         # noqa: E402

EXEMPLO = os.path.join(RAIZ, "exemplos", "mariana-fisioterapia")
CLI = os.path.join(RAIZ, "mindmestre")


def _build():
    mapa = Cartografo().destrinchar(EXEMPLO)
    det = Detetive().investigar(mapa)
    obj = Cetico().objetar(mapa, det)
    defs = Convicto().defender(mapa, det)
    juizo = Juiz().decidir(mapa, det, obj, defs)
    mkt = GenioMarketing().estudar(mapa)
    pos = Posicionador().posicionar(mapa, mkt)
    oferta = Copista().escrever(mapa, mkt, pos, det)
    ct = Conteudista().montar(mapa, mkt)
    plano = Estrategista().estruturar({"mapa": mapa, "det": det, "mkt": mkt, "pos": pos,
                                        "oferta": oferta, "ct": ct, "juizo": juizo})
    return mapa, det, juizo, mkt, pos, oferta, ct, plano


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapa, cls.det, cls.juizo, cls.mkt, cls.pos, cls.oferta, cls.ct, cls.plano = _build()


class TestArte(Base):
    def test_banner(self):
        linhas = bloco()
        self.assertEqual(len(linhas), 6)
        tinta = sum(sum(1 for c in l if c in "█═║╗╝╔╚╩╦╬") for l in linhas)
        self.assertGreater(tinta, 150)
        for l in linhas:
            self.assertGreater(len(l), 20)


class TestLeitura(Base):
    def test_caminhos_e_texto(self):
        arqs = leitura_pessoal.listar_arquivos(EXEMPLO)
        self.assertGreaterEqual(len(arqs), 3)
        txt = leitura_pessoal.ler_texto(os.path.join(EXEMPLO, "notas", "entrevista.md"))
        self.assertGreater(len(leitura_pessoal.frases(txt)), 3)
        self.assertEqual(leitura_pessoal.normalizar("Você está Travado?"), "voce esta travado?")


class TestPadroes(Base):
    def test_sinais_plantados(self):
        tipos = {s["tipo"] for s in self.mapa["sinais"]}
        for esperado in ("exposicao", "procrastinacao", "oferta", "desvalorizacao", "validacao", "dispersao"):
            self.assertIn(esperado, tipos)
        for s in self.mapa["sinais"]:
            self.assertTrue(s.get("arquivo"))
            self.assertTrue(s.get("trecho"))
        ativos = {a["tipo"] for a in self.mapa["ativos"]}
        for esperado in ("especialidade", "audiencia", "portefolio", "prova_social", "demanda"):
            self.assertIn(esperado, ativos)
        self.assertIn("curso", self.mapa["produtos_mentionados"])
        self.assertGreaterEqual(len(self.mapa["produtos_mentionados"]), 4)


class TestCartografo(Base):
    def test_mapa(self):
        self.assertEqual(self.mapa["persona_nome"], "Mariana")
        self.assertIn("postura", self.mapa["objetivo_declarado"])
        self.assertTrue(self.mapa["quero_produto"])
        self.assertGreater(self.mapa["palavras"], 100)
        self.assertTrue(self.mapa["resumo"])


class TestDetetive(Base):
    def test_hipotese_principal(self):
        self.assertGreaterEqual(len(self.det["hipoteses"]), 4)
        self.assertEqual(self.det["principal"], "exposicao")
        top = [h for h in self.det["hipoteses"] if h["id"] == "exposicao"][0]
        self.assertGreaterEqual(len(top["evidencias"]), 1)
        self.assertTrue(any("rirem" in e["trecho"] for e in top["evidencias"]))
        self.assertGreaterEqual(len(self.det["perguntas_abertas"]), 1)


class TestTribunal(Base):
    def test_veredito(self):
        self.assertIsInstance(self.juizo["confianca"], int)
        self.assertTrue(5 <= self.juizo["confianca"] <= 99)
        self.assertEqual(len(self.juizo["barra"]), 20)
        self.assertIn("pena", self.juizo["pontuacao"])
        self.assertIn("ganho", self.juizo["pontuacao"])
        self.assertTrue(self.juizo["decisao"])
        self.assertGreaterEqual(len(self.juizo["objecoes"]), 3)
        self.assertGreaterEqual(len(self.juizo["defesas"]), 3)


class TestMarketing(Base):
    def test_nicho_persona_empatia(self):
        self.assertIn("postura", self.mkt["nisca"])
        self.assertTrue(self.mkt["persona"]["codinome"])
        self.assertEqual(len(self.mkt["empatia"]), 8)
        self.assertGreaterEqual(len(self.mkt["canais"]), 1)
        self.assertTrue(self.mkt["icp"])


class TestPosicionamento(Base):
    def test_posicao(self):
        self.assertIn("Mariana", self.pos["sentenca"])
        self.assertEqual(len(self.pos["nomes"]), 5)
        self.assertTrue(self.pos["promessa"])
        self.assertGreaterEqual(len(self.pos["diferencadores"]), 3)


class TestCopista(Base):
    def test_corpus(self):
        self.assertGreaterEqual(len(CORPUS), 12)
        for c in CORPUS:
            for k in ("ano", "autor", "tecnica", "formula"):
                self.assertIn(k, c)

    def test_oferta(self):
        self.assertIn(self.oferta["estagio_mercado"], (1, 2, 3, 4, 5))
        self.assertGreaterEqual(len(self.oferta["headlines"]), 3)
        for h in self.oferta["headlines"]:
            self.assertTrue(h["texto"] and h["tecnica"])
        self.assertIn("100%", self.oferta["reversao_risco"])
        self.assertEqual(len(self.oferta["pagina"]), 8)
        self.assertTrue(self.oferta["cta"])
        self.assertGreaterEqual(len(self.oferta["corpus_usados"]), 3)


class TestConteudo(Base):
    def test_maquina(self):
        self.assertEqual(len(self.ct["hooks"]), 10)
        self.assertEqual(len(self.ct["pilares"]), 4)
        self.assertEqual(len(self.ct["calendario"]), 4)
        self.assertEqual(len(self.ct["stepps"]), 6)
        self.assertGreaterEqual(len(self.ct["kpis"]), 3)
        for w in self.ct["calendario"]:
            self.assertGreaterEqual(len(w["posts"]), 3)


class TestEstrategista(Base):
    SLUGS = ["diagnostico", "mapa-da-casa", "posicionamento-e-oferta",
             "pessoas-e-mercado", "maquina-de-conteudo", "voo"]

    def test_fases(self):
        self.assertEqual([f["slug"] for f in self.plano["fases"]], self.SLUGS)
        for f in self.plano["fases"]:
            self.assertTrue(f["blocos"])

    def test_curso(self):
        c = self.plano["curso"]
        self.assertTrue(c["ativo"])
        self.assertEqual(len(c["modulos"]), 6)
        for m in c["modulos"]:
            self.assertGreaterEqual(len(m["aulas"]), 4)
            self.assertTrue(m["resultado"])

    def test_voo(self):
        self.assertEqual(len(self.plano["voo_30_60_90"]), 3)
        self.assertEqual(len(self.plano["passos_hoje"]), 3)
        self.assertEqual(len(self.plano["prompts"]), 3)


class TestMermaid(Base):
    def test_diagramas(self):
        mm = mermaid.mapa_mermaid(self.mapa)
        self.assertIn("flowchart TD", mm)
        self.assertIn("P([", mm)
        pm = mermaid.plano_mermaid(self.plano)
        self.assertIn("flowchart TD", pm)
        self.assertIn("Fase 1", pm)
        self.assertIn("Fase 6", pm)


class TestRelatorios(Base):
    def test_sete_artefatos(self):
        tmp = tempfile.mkdtemp(prefix="mind_test_")
        try:
            caminhos = relatorios.escrever_tudo(tmp, self.plano, self.mapa)
            for k in ("pdf", "docx", "md", "mapa_json", "mmd_mapa", "mmd_plano", "obsidian"):
                self.assertTrue(os.path.exists(caminhos[k]), k)
            pdf_b = open(caminhos["pdf"], "rb").read()
            self.assertTrue(pdf_b.startswith(b"%PDF"), "header do PDF")
            try:
                from pypdf import PdfReader
                self.assertGreaterEqual(len(PdfReader(io.BytesIO(pdf_b)).pages), 3)
            except ImportError:
                pass
            docx_b = open(caminhos["docx"], "rb").read()
            try:
                import docx as pydocx
                self.assertTrue(pydocx.Document(io.BytesIO(docx_b)).paragraphs)
            except ImportError:
                with zipfile.ZipFile(io.BytesIO(docx_b)) as z:
                    self.assertIn("word/document.xml", z.namelist())
            md = open(caminhos["md"], encoding="utf-8").read()
            self.assertIn("## Fase 1", md)
            self.assertIn("```json", md)
            notas = sorted(os.listdir(caminhos["obsidian"]))
            self.assertEqual(len(notas), 9)
            bases = {n[:-3] for n in notas}
            for n in notas:
                conteudo = open(os.path.join(caminhos["obsidian"], n), encoding="utf-8").read()
                for alvo in re.findall(r"\[\[([^\]|]+)", conteudo):
                    self.assertIn(alvo.strip(), bases, "wikilink pendente: %s em %s" % (alvo, n))
            mapa_j = json.load(open(caminhos["mapa_json"], encoding="utf-8"))
            self.assertEqual(mapa_j["persona_nome"], "Mariana")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestInquisidor(Base):
    def test_nuance(self):
        tecnico = medir_nuance("Minha hipótese é de que o mercado responde à oferta; se eu validar o MVP e o funil converte, o preço sobe")
        hesita = medir_nuance("acho que... não sei... tipo assim, estou meio travado")
        self.assertGreater(tecnico["nivel"], hesita["nivel"])
        self.assertTrue(1 <= hesita["nivel"] <= 5)

    def test_estado(self):
        inq = Inquisidor()
        est = inq.estado_inicial(None, "abertura")
        q1 = inq.pergunta(est)
        self.assertTrue(q1.endswith("?"))
        q2 = inq.responder(est, "quero criar um curso e tenho medo de aparecer")
        self.assertNotEqual(q1, q2)
        self.assertGreaterEqual(est["rodada"], 1)


class TestLlm(Base):
    def test_offline(self):
        self.assertIsNone(llm.detectar())
        r = llm.chamar("sistema", "usuario")
        self.assertTrue(r is None or isinstance(r, str))


class TestCli(Base):
    def _run(self, args, inp=None):
        env = dict(os.environ)
        env["MIND_SEM_IA"] = "1"
        return subprocess.run([sys.executable, CLI] + args, input=inp,
                              capture_output=True, text=True, env=env, cwd=RAIZ, timeout=180)

    def test_arte_status_versao(self):
        r = self._run(["arte"])
        self.assertEqual(r.returncode, 0)
        r = self._run(["status"])
        self.assertEqual(r.returncode, 0, r.stderr[-500:])
        self.assertIn("Cético", r.stdout)
        self.assertIn("offline", r.stdout)
        r = self._run(["versao"])
        self.assertEqual(r.returncode, 0)

    def test_mapa(self):
        tmp = tempfile.mkdtemp(prefix="mind_cli_")
        try:
            r = self._run(["mapa", EXEMPLO, "-o", tmp])
            self.assertEqual(r.returncode, 0, r.stderr[-800:])
            self.assertTrue(os.path.exists(os.path.join(tmp, "mapa.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp, "mapa.mmd")))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_plano(self):
        tmp = tempfile.mkdtemp(prefix="mind_plan_")
        try:
            r = self._run(["plano", EXEMPLO, "--sem-ia", "-o", tmp])
            self.assertEqual(r.returncode, 0, r.stderr[-1200:])
            for nome in ("plano.pdf", "plano.docx", "plano.md", "mapa.json", "mapa.mmd", "plano.mmd"):
                self.assertTrue(os.path.exists(os.path.join(tmp, nome)), nome)
            self.assertTrue(os.path.isdir(os.path.join(tmp, "obsidian")))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_conversa_pipeada(self):
        tmp = tempfile.mkdtemp(prefix="mind_conv_")
        try:
            r = self._run(["conversa", "--rodadas", "2", "-o", tmp],
                          inp="quero criar um curso sobre postura\nme dá medo de aparecer na câmera\n")
            self.assertEqual(r.returncode, 0, r.stderr[-800:])
            self.assertTrue(os.path.exists(os.path.join(tmp, "conversa.md")))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestPacoteAgentes(Base):
    ARQ = ["cartografo", "detetive", "estrategista", "marketing", "inquisidor",
           "posicionamento", "conteudo", "copista", "cetico", "convicto", "juiz",
           "__init__", "comum"]

    def test_um_arquivo_por_agente(self):
        presentes = set(os.listdir(os.path.join(RAIZ, "agentes")))
        for a in self.ARQ:
            self.assertIn(a + ".py", presentes)
        self.assertIn("README.md", presentes)
        import importlib
        for mod in ("agentes.cartografo", "agentes.detetive", "agentes.copista", "agentes.juiz"):
            importlib.import_module(mod)


if __name__ == "__main__":
    unittest.main(verbosity=2)
