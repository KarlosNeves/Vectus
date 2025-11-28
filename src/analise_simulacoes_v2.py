# analise_simulacoes_v2.py
"""
Motor de simulação do Projeto Tributec — v2.0
Compatível com config.json personalizado - CORRIGIDO
"""

import csv
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# ===========================
# FUNÇÕES CORE
# ===========================

def criar_diretorio_saida(config: dict):
    """Cria diretório de saída se não existir"""
    os.makedirs(config['output_dir'], exist_ok=True)
    print(f"📁 Diretório de saída: {config['output_dir']}")

def gerar_importacao(config: dict) -> dict:
    """Gera uma operação de importação simulada compatível com seu config"""
    # Usa faixas do seu config para gerar valores realistas
    faixas = config['faixas_valor_fob']
    
    # CORREÇÃO: Escolhe um índice aleatório em vez da faixa diretamente
    indice_faixa = np.random.randint(0, len(faixas) - 1)  # Exclui "ARROMBADO" que tem null
    min_val, max_val, classificacao = faixas[indice_faixa]
    
    valor_fob_usd = np.random.uniform(min_val, max_val)
    cambio = np.random.uniform(4.5, 6.5)  # Cambio realista
    
    # Usa NCMs do seu foco
    ncm = str(np.random.choice(config['ncm_foco']))
    
    # Cálculos com suas taxas fixas
    valor_fob_brl = valor_fob_usd * cambio
    ii_valor = valor_fob_brl * config['taxas']['ii_fixo']
    ipi_valor = valor_fob_brl * config['taxas']['ipi_fixo']
    pis_cofins_valor = valor_fob_brl * config['taxas']['pis_cofins_fixo']
    
    # ICMS varia por estado (simulação)
    aliquota_icms = np.random.choice([0.12, 0.17, 0.18])
    icms_valor = valor_fob_brl * aliquota_icms
    
    total_tributos = ii_valor + ipi_valor + pis_cofins_valor + icms_valor
    
    return {
        "valor_fob_usd": round(valor_fob_usd, 2),
        "cambio": round(cambio, 2),
        "valor_fob_brl": round(valor_fob_brl, 2),
        "ii_valor": round(ii_valor, 2),
        "ipi_valor": round(ipi_valor, 2),
        "pis_cofins_valor": round(pis_cofins_valor, 2),
        "icms_valor": round(icms_valor, 2),
        "total_tributos": round(total_tributos, 2),
        "ncm": ncm,
        "aliquota_icms": aliquota_icms
    }

def calcular_ict(total_tributos: float, valor_fob_brl: float, benchmark: float = 0.20) -> float:
    """Calcula o Índice de Carga Tributária com SEU benchmark"""
    if valor_fob_brl == 0:
        return 0.0
    carga_efetiva = total_tributos / valor_fob_brl
    return round(carga_efetiva / benchmark, 3)

def classificar_ict(ict: float) -> str:
    """Classifica o ICT em categorias"""
    if ict >= 2.0:
        return "🚨 ARROMBADO"
    elif ict >= 1.5:
        return "🔴 Crítico"
    elif ict >= 1.0:
        return "🟡 Alto"
    elif ict >= 0.5:
        return "🟢 Moderado"
    else:
        return "🔵 Baixo"

def classificar_carga_tributaria(total_tributos: float, faixas: list) -> str:
    """Classifica pela carga tributária total baseado nas suas faixas"""
    for faixa in faixas:
        min_val, max_val, classificacao = faixa
        if max_val is None:  # Última faixa (ARROMBADO)
            if total_tributos >= min_val:
                return classificacao
        elif min_val <= total_tributos < max_val:
            return classificacao
    return "INDEFINIDO"

def recomendar_estrategia(operacao: dict, config: dict) -> str:
    """Gera recomendação estratégica baseada na operação"""
    ict = operacao.get('ict', 0)
    valor_fob_usd = operacao.get('valor_fob_usd', 0)
    classificacao_carga = classificar_carga_tributaria(
        operacao.get('total_tributos', 0), 
        config['faixas_valor_fob']
    )
    
    if classificacao_carga == "ARROMBADO" or ict >= 2.0:
        return "🚨 URGENTE: Drawback + Revisão NCM + Consultoria Jurídica"
    elif classificacao_carga == "FODA" or ict >= 1.5:
        return "🔴 Revisar: Drawback + Otimização ICMS"
    elif valor_fob_usd > 1000000:
        return "🟡 Estudar Drawback - Valor elevado"
    elif "8471" in operacao.get('ncm', ''):
        return "🟢 Computadores - Verificar reduções setoriais"
    else:
        return "✅ Dentro dos parâmetros"

# ===========================
# FUNÇÕES PRINCIPAIS
# ===========================

def foder_sistema_com_simulacoes(n: int, config: dict) -> list:
    print(f"💥 Iniciando {n} simulações do Tributec...")
    importacoes = []
    for i in range(n):
        op = gerar_importacao(config)
        op['ict'] = calcular_ict(
            op['total_tributos'],
            op['valor_fob_brl'],
            config['benchmark_ict']
        )
        op['classificacao_ict'] = classificar_ict(op['ict'])
        op['classificacao_carga'] = classificar_carga_tributaria(
            op['total_tributos'], 
            config['faixas_valor_fob']
        )
        op['recomendacao'] = recomendar_estrategia(op, config)
        importacoes.append(op)
    print(f"✅ {len(importacoes)} operações simuladas com sucesso!")
    return importacoes

def salvar_csv(importacoes: list, caminho: str):
    if not importacoes:
        print("⚠️ Nenhuma operação pra salvar.")
        return

    campos = [
        "valor_fob_usd", "cambio", "valor_fob_brl", "ii_valor", "ipi_valor",
        "pis_cofins_valor", "icms_valor", "total_tributos", "ncm", "aliquota_icms",
        "ict", "classificacao_ict", "classificacao_carga", "recomendacao"
    ]

    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(importacoes)
    print(f"📁 CSV salvo: {caminho}")

def plotar_distribuicao(importacoes: list, caminho: str, faixas: list):
    tributos = [op["total_tributos"] for op in importacoes]
    plt.figure(figsize=(12, 7))
    
    # Histograma
    plt.hist(tributos, bins=50, alpha=0.7, color='#1f77b4', edgecolor='black')
    
    # Linhas das faixas do seu config
    cores = ['green', 'orange', 'red', 'purple']
    for i, (min_val, max_val, label) in enumerate(faixas):
        if max_val is not None:
            plt.axvline(max_val, color=cores[i], linestyle='--', 
                       label=f'{label} (R$ {max_val:,.0f})', linewidth=2)
        else:
            plt.axvline(min_val, color=cores[i], linestyle='--', 
                       label=f'{label} (≥R$ {min_val:,.0f})', linewidth=2)
    
    plt.title('Distribuição de Carga Tributária - Com Suas Faixas Personalizadas', fontsize=14)
    plt.xlabel('Total de Tributos (R$)')
    plt.ylabel('Frequência')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"🖼️ Gráfico salvo: {caminho}")

def gerar_relatorio_html(importacoes: list, config: dict, caminho: str):
    tributos = [op['total_tributos'] for op in importacoes]
    icts = [op['ict'] for op in importacoes]
    
    media_tributos = sum(tributos) / len(tributos)
    media_ict = sum(icts) / len(icts)
    
    # Contagens baseadas nas SUAS faixas
    leve = len([op for op in importacoes if op['classificacao_carga'] == 'LEVE'])
    medio = len([op for op in importacoes if op['classificacao_carga'] == 'MÉDIO'])
    foda = len([op for op in importacoes if op['classificacao_carga'] == 'FODA'])
    arrombado = len([op for op in importacoes if op['classificacao_carga'] == 'ARROMBADO'])
    
    criticos_ict = len([op for op in importacoes if op['classificacao_ict'] in ['🚨 ARROMBADO', '🔴 Crítico']])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Relatório Tributec — {datetime.now():%Y-%m-%d}</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; max-width: 1000px; margin: 20px auto; }}
            .card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }}
            .alerta {{ color: #d9534f; font-weight: bold; }}
            .critico {{ color: #ff6b35; font-weight: bold; }}
            .ok {{ color: #5cb85c; font-weight: bold; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        </style>
    </head>
    <body>
        <h1>🎯 Relatório Tributec — Config Personalizada</h1>
        <p><em>Gerado em {datetime.now():%d/%m/%Y às %H:%M}</em></p>

        <div class="grid">
            <div class="card">
                <h2>📊 Resumo por Carga</h2>
                <p><strong>LEVE:</strong> <span class="ok">{leve} ({leve/len(importacoes)*100:.1f}%)</span></p>
                <p><strong>MÉDIO:</strong> <span>{medio} ({medio/len(importacoes)*100:.1f}%)</span></p>
                <p><strong>FODA:</strong> <span class="critico">{foda} ({foda/len(importacoes)*100:.1f}%)</span></p>
                <p><strong>ARROMBADO:</strong> <span class="alerta">{arrombado} ({arrombado/len(importacoes)*100:.1f}%)</span></p>
            </div>

            <div class="card">
                <h2>📈 Métricas ICT</h2>
                <p><strong>ICT Médio:</strong> {media_ict:.2f}</p>
                <p><strong>Benchmark:</strong> {config['benchmark_ict']}</p>
                <p><strong>Críticos/Arrombados:</strong> <span class="alerta">{criticos_ict}</span></p>
                <p><strong>Carga Média:</strong> R$ {media_tributos:,.0f}</p>
            </div>
        </div>

        <div class="card">
            <h2>📊 Gráfico - Suas Faixas</h2>
            <img src="distribuicao_tributos.png" width="100%">
        </div>

        <div class="card">
            <h2>🔍 NCMs em Foco</h2>
            <p><strong>Setores analisados:</strong> {', '.join(config['ncm_foco'])}</p>
            <p><strong>Taxas aplicadas:</strong> II {config['taxas']['ii_fixo']*100}%, IPI {config['taxas']['ipi_fixo']*100}%, PIS/COFINS {config['taxas']['pis_cofins_fixo']*100}%</p>
        </div>

        <div class="card">
            <h2>🎯 Recomendações Estratégicas</h2>
            <p>Operações <span class="alerta">ARROMBADAS</span>: Prioridade máxima para drawback e revisão jurídica</p>
            <p>Setor <strong>{config['ncm_foco'][0]}</strong>: Verificar incentivos fiscais setoriais</p>
            <p>Potencial de economia: <strong>R$ {(arrombado * 250000 + foda * 80000):,.0f}</strong></p>
        </div>

        <footer style="text-align: center; margin-top: 30px; color: #666;">
            <p>Tributec v2.0 — Config personalizada — "Sistema fodido com sucesso!"</p>
        </footer>
    </body>
    </html>
    """
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"📄 Relatório HTML gerado: {caminho}")

# ===========================
# EXECUÇÃO PRINCIPAL
# ===========================
if __name__ == "__main__":
    print("🚀 Iniciando Tributec v2.0 com config personalizada...")

    # Carrega SEU config.json
    try:
        with open('config.json', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ Configuração personalizada carregada!")
    except FileNotFoundError:
        print("❌ config.json não encontrado. Execute novamente com seu arquivo.")
        exit(1)

    # Prepara saída
    criar_diretorio_saida(config)

    # Simula
    importacoes = foder_sistema_com_simulacoes(config['simulacoes'], config)

    # Gera artefatos
    csv_path = f"{config['output_dir']}simulacoes_com_ict.csv"
    png_path = f"{config['output_dir']}distribuicao_tributos.png"
    html_path = f"{config['output_dir']}relatorio.html"

    salvar_csv(importacoes, csv_path)
    plotar_distribuicao(importacoes, png_path, config['faixas_valor_fob'])
    gerar_relatorio_html(importacoes, config, html_path)

    print("\n🎯 TRIBUTEC v2.0 — EXECUTADO COM SUA CONFIG!")
    print(f"📊 {config['simulacoes']} simulações com benchmark ICT {config['benchmark_ict']}")
    print(f"📁 Resultados em: {config['output_dir']}")
    print(f"➡️  Abra '{html_path}' no navegador!")