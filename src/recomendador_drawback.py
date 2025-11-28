# recomendador_drawback.py
"""
Módulo especializado em análise de elegibilidade e potencial do regime DRAWBACK.
Compatível com 'operacoes_reais_simuladas.csv' gerado por 'analise_dados_reais.py'.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def verificar_vinculacao(importacoes: pd.DataFrame, exportacoes: pd.DataFrame,
                        cnpj: str, tolerancia_tempo_dias: int = 365) -> pd.DataFrame:
    """
    Verifica vinculação importação-exportação por CNPJ, NCM e janela temporal.
    Regra: exportação até 365 dias após importação, com ≥90% da quantidade.
    """
    imp = importacoes[importacoes['cnpj_basico'] == cnpj].copy()
    exp = exportacoes[exportacoes['cnpj_basico'] == cnpj].copy()
    
    if imp.empty or exp.empty:
        return pd.DataFrame()
    
    vinculos = []
    for _, imp_row in imp.iterrows():
        exp_match = exp[
            (exp['ncm'] == imp_row['ncm']) &
            (exp['data_exportacao'] >= imp_row['data_importacao']) &
            (exp['data_exportacao'] <= imp_row['data_importacao'] + timedelta(days=tolerancia_tempo_dias)) &
            (exp['quantidade'] >= 0.9 * imp_row['quantidade'])
        ]
        
        for _, exp_row in exp_match.iterrows():
            vinculos.append({
                'cnpj_basico': cnpj,
                'ncm': imp_row['ncm'],
                'data_importacao': imp_row['data_importacao'],
                'valor_fob_brl_imp': imp_row['valor_fob_brl'],
                'ii_pago': imp_row['ii_valor'],
                'ipi_pago': imp_row['ipi_valor'],
                'data_exportacao': exp_row['data_exportacao'],
                'quantidade_imp': imp_row['quantidade'],
                'quantidade_exp': exp_row['quantidade'],
                'proporcao': round(exp_row['quantidade'] / imp_row['quantidade'], 2)
            })
    return pd.DataFrame(vinculos)

def calcular_economia_drawback(ii_valor: float, ipi_valor: float,
                             tipo_drawback: str = 'isencao') -> dict:
    economia = ii_valor + ipi_valor
    return {
        'economia_ii': ii_valor,
        'economia_ipi': ipi_valor,
        'economia_total': economia,
        'tipo_drawback_aplicavel': tipo_drawback
    }

def checklist_documentos(empresa: pd.Series) -> list:
    faltantes = []
    # Dados fictícios, já que não temos no CSV atual — só exemplo funcional
    if empresa.get('capital_social_real', 0) > 1_000_000:
        faltantes.append("✅ Sistema de controle de produção (obrigatório para Isenção)")
    if empresa.get('porte_empresa') == '3':  # Médio/Grande
        faltantes.append("✅ Registro no CMC (Manifestante)")
    return faltantes

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print("🔍 INICIANDO ANÁLISE DE ELEGIBILIDADE AO DRAWBACK...")
    
    # Carrega dados
    try:
        df = pd.read_csv('./output/operacoes_reais_simuladas.csv')
    except FileNotFoundError:
        print("❌ Arquivo 'operacoes_reais_simuladas.csv' não encontrado.")
        print("➡️  Execute 'analise_dados_reais.py' primeiro.")
        exit(1)

    # 🔧 CORREÇÃO: Adiciona colunas obrigatórias que faltam no CSV atual
    if 'tipo_operacao' not in df.columns:
        print("⚠️  Coluna 'tipo_operacao' ausente → assumindo todas como 'importacao'.")
        df['tipo_operacao'] = 'importacao'

    # Garante colunas de tributos (como no seu simulador)
    if 'ii_valor' not in df.columns:
        df['ii_valor'] = df['valor_fob_brl'] * 0.02    # II 2%
    if 'ipi_valor' not in df.columns:
        df['ipi_valor'] = df['valor_fob_brl'] * 0.05   # IPI 5%

    # Base de data para simulação (2024)
    base_date = pd.to_datetime('2024-01-01')
    df['data_importacao'] = base_date + pd.to_timedelta(
        np.random.randint(0, 300, len(df)), unit='D'
    )
    df['quantidade'] = 100  # 100 unidades por operação (base)

    # 🔄 GERA EXPORTAÇÕES SIMULADAS (apenas para teste de Drawback)
    print("🔄 Gerando exportações simuladas para análise de vinculação...")
    df_imp = df[df['tipo_operacao'] == 'importacao'].copy()
    
    # Seleciona ~30% das importações para ter exportações vinculáveis
    np.random.seed(42)
    mask_export = np.random.random(len(df_imp)) < 0.3
    df_exp = df_imp[mask_export].copy()
    
    df_exp['tipo_operacao'] = 'exportacao'
    df_exp['data_exportacao'] = df_exp['data_importacao'] + pd.to_timedelta(
        np.random.randint(30, 365, len(df_exp)), unit='D'
    )
    df_exp['quantidade'] = np.random.randint(90, 101, len(df_exp))  # 90-100%
    df_exp['ii_valor'] = 0.0
    df_exp['ipi_valor'] = 0.0

    # Junta importações + exportações simuladas
    df_completo = pd.concat([df_imp, df_exp], ignore_index=True)
    importacoes = df_completo[df_completo['tipo_operacao'] == 'importacao'].copy()
    exportacoes = df_completo[df_completo['tipo_operacao'] == 'exportacao'].copy()

    print(f"✅ Base preparada: {len(importacoes)} importações + {len(exportacoes)} exportações")

    # Analisa elegibilidade
    cnpjs_candidatos = set(importacoes['cnpj_basico']) & set(exportacoes['cnpj_basico'])
    print(f"📌 {len(cnpjs_candidatos)} empresas com operações de importação e exportação.")

    resultados = []
    for cnpj in cnpjs_candidatos:
        vinculos = verificar_vinculacao(importacoes, exportacoes, cnpj)
        if not vinculos.empty:
            ii_total = vinculos['ii_pago'].sum()
            ipi_total = vinculos['ipi_pago'].sum()
            economia = calcular_economia_drawback(ii_total, ipi_total)
            
            emp_data = df_completo[df_completo['cnpj_basico'] == cnpj].iloc[0]
            
            resultado = {
                'cnpj_basico': cnpj,
                'razao_social': emp_data['razao_social'],
                'porte': emp_data['porte_empresa'],
                'capital_social': emp_data['capital_social_real'],
                'total_ii_importado': ii_total,
                'total_ipi_importado': ipi_total,
                'economia_drawback_estimada': economia['economia_total'],
                'tipo_drawback_recomendado': economia['tipo_drawback_aplicavel'],
                'ncms_vinculaveis': ', '.join(sorted(vinculos['ncm'].astype(str).unique())),
                'qtd_vinculos': len(vinculos),
                'documentos_faltantes': '; '.join(checklist_documentos(emp_data))
            }
            resultados.append(resultado)

    # Salva resultados
    os.makedirs('./output', exist_ok=True)
    
    if resultados:
        df_drawback = pd.DataFrame(resultados)
        df_drawback.to_csv('./output/empresas_drawback_elegiveis.csv', index=False, encoding='utf-8')
        
        total_economia = df_drawback['economia_drawback_estimada'].sum()
        print(f"✅ {len(df_drawback)} empresas elegíveis ao Drawback identificadas.")
        print(f"💰 Economia total estimada: R$ {total_economia:,.2f}")
        
        # Gera HTML (minimalista, mas claro)
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Drawback - Análise de Elegibilidade</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }}
.container {{ max-width: 1000px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
.header {{ background: #2980b9; color: white; padding: 20px; text-align: center; border-radius: 8px; margin-bottom: 20px; }}
.empresa {{ border-left: 4px solid #3498db; margin: 15px 0; padding: 15px; background: #f8f9fa; }}
.highlight {{ color: #c0392b; font-weight: bold; }}
</style></head><body>
<div class="container">
    <div class="header">
        <h1>🎯 ANÁLISE DRAWBACK — ELEGIBILIDADE REAL</h1>
        <p>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    <p><strong>{len(df_drawback)}</strong> empresas elegíveis | Economia potencial: 
       <span class="highlight">R$ {total_economia:,.2f}</span></p>
"""
        for _, emp in df_drawback.iterrows():
            html += f"""
    <div class="empresa">
        <h3>🏭 {emp['razao_social']}</h3>
        <p><strong>CNPJ:</strong> {emp['cnpj_basico']} | <strong>Porte:</strong> {emp['porte']} | <strong>Capital:</strong> R$ {emp['capital_social']:,.0f}</p>
        <p>💰 <strong>Economia:</strong> R$ {emp['economia_drawback_estimada']:,.2f} (II: R$ {emp['total_ii_importado']:,.2f} + IPI: R$ {emp['total_ipi_importado']:,.2f})</p>
        <p>📦 <strong>NCMs:</strong> {emp['ncms_vinculaveis']}</p>
        <p>📋 <strong>Documentos:</strong> {emp['documentos_faltantes'] or 'Nenhum crítico'}</p>
    </div>"""
        
        html += "</div></body></html>"
        
        with open('./output/relatorio_drawback.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("📁 Arquivos gerados:")
            # 🔥 ABRE O RELATÓRIO AUTOMATICAMENTE (Windows)
        import os
        relatorio_path = os.path.abspath('./output/relatorio_drawback.html')
        print(f"\n🚀 Abrindo relatório em seu navegador...")
        os.startfile(relatorio_path)  # Windows-only, mas perfeito pro seu setup!
        print("   - ./output/empresas_drawback_elegiveis.csv")
        print("   - ./output/relatorio_drawback.html")
    
    else:
        print("❌ Nenhuma empresa elegível ao Drawback encontrada.")
        print("💡 Dica: aumente o número de operações ou ajuste a simulação para incluir mais exportações.")