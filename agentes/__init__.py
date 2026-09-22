# -*- coding: utf-8 -*-
"""agentes — o time do Mind Mestre, um agente por arquivo.

Mesma arquitetura do Instalador: motor determinístico, pontuação aberta,
evidência com endereço (arquivo:linha). O LLM, quando presente, refina
prosa — nunca decide sozinho. Ordem do tribunal: Cético × Convicto × Juiz
antes de qualquer coisa decolar."""
from .cartografo import Cartografo
from .detetive import Detetive
from .inquisidor import Inquisidor
from .marketing import GenioMarketing
from .posicionamento import Posicionador
from .copista import Copista
from .conteudo import Conteudista
from .estrategista import Estrategista
from .cetico import Cetico
from .convicto import Convicto
from .juiz import Juiz

__all__ = ["Cartografo", "Detetive", "Inquisidor", "GenioMarketing",
           "Posicionador", "Copista", "Conteudista", "Estrategista",
           "Cetico", "Convicto", "Juiz"]
