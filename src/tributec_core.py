# tributec_core.py
"""
Módulo central do Projeto Tributec — lógica reutilizável, limpa e fiscalmente precisa.
"""

import random
from pathlib import Path
from typing import List, Dict

def icms_importacao_rj(valor_fob_usd: float, cambio: float, aliquota: float = 0.20) -> Dict:
    """Calcula ICMS de importação para RJ (baseado em legislação vigente)"""
    valor_fob_brl = valor_fob_usd * cambio
    ii_valor = valor_fob_brl * 0.05
    base_icms = valor_fob_brl + ii_valor
    icms_valor = base_icms * aliquota
    return {
        "valor_fob_usd": valor_fob_usd,
        "cambio": cambio,
        "valor_fob_brl": valor_fob_brl,
        "ii_valor": ii_valor,
        "icms_valor": icms_valor,
        "total_tributos": ii_valor + icms_valor
    }

def gerar_importacao(config: dict) -> Dict:
    """Gera uma operação de importação aleatória, mas realista"""
    fob = random.uniform(10_000, 1_000_000)
    cambio = random.uniform(4.5, 6.5)
    aliquota = random.choice([0.17, 0.18, 0.19, 0.20])
    ncm = random.choice(config.get("ncm_foco", ["8471"]))

    op = icms_importacao_rj(fob, cambio, aliquota)
    op.update({
        "ncm": ncm,
        "aliquota_icms": aliquota
    })
    return op

def calcular_ict(total_tributos: float, valor_fob_brl: float, benchmark: float) -> float:
    """Calcula o Índice de Complexidade Tributária (ICT)"""
    carga_efetiva = total_tributos / valor_fob_brl
    return abs(carga_efetiva - benchmark) * 100

def classificar_ict(ict: float) -> str:
    """Classifica o ICT em faixas estratégicas"""
    if ict <= 5:   return "✅ Eficiente"
    elif ict <= 15: return "⚠️ Moderado"
    else:           return "🚨 Crítico"

def recomendar_estrategia(op: dict, config: dict) -> str:
    """Gera recomendação fiscal com base no perfil da operação"""
    if op['ict'] > 15 and op['valor_fob_usd'] > 800_000:
        return "🚨 Revisar regime aduaneiro + análise de drawback"
    elif op['ncm'] in ["8471", "8517"] and op['ict'] > 10:
        return "🔧 Verificar classificação fiscal (NCM crítico)"
    else:
        return "✅ Manter estrutura — eficiência comprovada"

def criar_diretorio_saida(config: dict):
    """Cria pasta de saída, se não existir"""
    Path(config["output_dir"]).mkdir(exist_ok=True)
