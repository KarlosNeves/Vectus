# arquivo: analise_dados_reais.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

print("🔍 Carregando dados REAIS da Receita Federal...")

# CAMINHO CORRETO - baseado na sua estrutura
CAMINHO_CORRETO = "./data/empresas_rf.txt"

try:
    df_real = pd.read_csv(
        CAMINHO_CORRETO,
        sep=';',
        encoding='latin1',
        header=None,
        names=[
            'cnpj_basico',
            'razao_social',
            'natureza_juridica',
            'qualificacao_responsavel', 
            'capital_social',
            'porte_empresa',
            'ente_federativo'
        ],
        on_bad_lines='skip',
        nrows=10000,  # Vamos começar com 10k empresas
        low_memory=False
    )
    
    print(f"✅ SUCESSO! {len(df_real)} empresas reais carregadas!")
    
    # Converte capital_social
    df_real['capital_social'] = pd.to_numeric(
        df_real['capital_social'].str.replace(',', '.'), 
        errors='coerce'
    ).fillna(0.0)
    
    print("\n📊 Estatísticas dos dados REAIS:")
    print(f"   - Capital social médio: R$ {df_real['capital_social'].mean():,.2f}")
    print(f"   - Capital social máximo: R$ {df_real['capital_social'].max():,.2f}")
    print(f"   - Portes de empresa: {df_real['porte_empresa'].value_counts().to_dict()}")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    exit(1)

# FUNÇÕES PARA SIMULAR IMPORTAÇÕES BASEADAS EM DADOS REAIS
def calcular_ict(total_tributos: float, valor_fob_brl: float, benchmark: float = 0.35) -> float:
    if valor_fob_brl == 0:
        return 0.0
    carga_efetiva = total_tributos / valor_fob_brl
    return round(carga_efetiva / benchmark, 3)

def classificar_ict(ict: float) -> str:
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

def simular_operacoes_reais(df_empresas, n_operacoes=1000):
    """Simula operações de importação baseadas em empresas REAIS"""
    print(f"\n💥 Simulando {n_operacoes} operações baseadas em dados REAIS...")
    
    operacoes = []
    empresas_com_capital = df_empresas[df_empresas['capital_social'] > 0]
    
    if len(empresas_com_capital) == 0:
        print("❌ Nenhuma empresa com capital social > 0 encontrada!")
        return []
    
    for i in range(n_operacoes):
        # Seleciona uma empresa REAL aleatória
        empresa = empresas_com_capital.sample(1).iloc[0]
        
        # Baseia o valor FOB no capital social REAL
        fator_importacao = np.random.uniform(0.1, 3.0)  # Empresa importa 10-300% do capital
        valor_fob_usd = (empresa['capital_social'] * fator_importacao) / 5.3  # Converte para USD
        
        # Garante valores mínimos realistas
        valor_fob_usd = max(5000, min(valor_fob_usd, 5000000))
        
        cambio = np.random.uniform(4.8, 5.8)
        valor_fob_brl = valor_fob_usd * cambio
        
        # Tributos com taxas realistas
        ii_valor = valor_fob_brl * 0.02    # II 2%
        ipi_valor = valor_fob_brl * 0.05   # IPI 5% 
        pis_cofins_valor = valor_fob_brl * 0.034  # PIS/COFINS 3.4%
        icms_valor = valor_fob_brl * np.random.choice([0.07, 0.12, 0.17])
        
        total_tributos = ii_valor + ipi_valor + pis_cofins_valor + icms_valor
        ict = calcular_ict(total_tributos, valor_fob_brl, 0.35)
        
        operacao = {
            "cnpj_basico": empresa['cnpj_basico'],
            "razao_social": empresa['razao_social'][:30] + "..." if len(empresa['razao_social']) > 30 else empresa['razao_social'],
            "capital_social_real": empresa['capital_social'],
            "porte_empresa": empresa['porte_empresa'],
            "valor_fob_usd": round(valor_fob_usd, 2),
            "cambio": round(cambio, 2),
            "valor_fob_brl": round(valor_fob_brl, 2),
            "total_tributos": round(total_tributos, 2),
            "ncm": np.random.choice(["8471", "8517", "9022"]),
            "ict": ict,
            "classificacao_ict": classificar_ict(ict)
        }
        operacoes.append(operacao)
    
    print(f"✅ {len(operacoes)} operações simuladas baseadas em empresas REAIS!")
    return operacoes

# EXECUTA A SIMULAÇÃO COM DADOS REAIS
operacoes_reais = simular_operacoes_reais(df_real, 1000)

if operacoes_reais:
    # Converte para DataFrame para análise
    df_operacoes = pd.DataFrame(operacoes_reais)
    
    print(f"\n🎯 RESULTADOS BASEADOS EM DADOS REAIS:")
    print(f"   📊 ICT Médio: {df_operacoes['ict'].mean():.2f}")
    print(f"   💰 Carga Tributária Média: R$ {df_operacoes['total_tributos'].mean():,.0f}")
    print(f"   🚨 Operações Críticas: {len(df_operacoes[df_operacoes['ict'] >= 1.5])}")
    print(f"   💸 Capital Social Médio das empresas: R$ {df_operacoes['capital_social_real'].mean():,.0f}")
    
    # Salva resultados
    df_operacoes.to_csv("./output/operacoes_reais_simuladas.csv", index=False)
    print(f"\n📁 Resultados salvos em: ./output/operacoes_reais_simuladas.csv")
    
else:
    print("❌ Não foi possível gerar operações.")