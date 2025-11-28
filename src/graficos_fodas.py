# graficos_fodas.py - VERSÃO CORRIGIDA
import matplotlib
matplotlib.use('Agg')  # 🔥 USA BACKEND SEM GUI - ADICIONA ISSO NO TOPO!
import matplotlib.pyplot as plt
import pandas as pd
from analise_simulacoes import importacoes

def criar_graficos_arrombados():
    """GRÁFICOS QUE VÃO FUDER, MAS SEM GUI"""
    if not importacoes:
        print("❌ GEROU OS DADOS PRIMEIRO, PORRA!")
        return
    
    print("🎨 CRIANDO GRÁFICOS FODAS (SALVANDO EM ARQUIVOS)...")
    
    # Converter pra DataFrame
    df = pd.DataFrame(importacoes)
    
    # 1. HISTOGRAMA DOS TRIBUTOS
    plt.figure(figsize=(10, 6))
    plt.hist(df['total_tributos'], bins=50, alpha=0.7, color='red', edgecolor='black')
    plt.title('DISTRIBUIÇÃO DOS TRIBUTOS - ARROMBADO TOTAL')
    plt.xlabel('Valor em R$')
    plt.ylabel('Frequência')
    plt.grid(True, alpha=0.3)
    plt.savefig('histograma_tributos.png')  # 🔥 SALVA EM ARQUIVO
    print("✅ HISTOGRAMA SALVO: histograma_tributos.png")
    plt.close()
    
    # 2. SCATTER PLOT: VALOR FOB vs TRIBUTOS
    plt.figure(figsize=(10, 6))
    plt.scatter(df['valor_fob_usd'], df['total_tributos'], alpha=0.5, color='blue')
    plt.title('VALOR FOB vs TRIBUTOS - CORRELAÇÃO FODA')
    plt.xlabel('Valor FOB (USD)')
    plt.ylabel('Tributos (R$)')
    plt.grid(True, alpha=0.3)
    plt.savefig('scatter_fob_tributos.png')
    print("✅ SCATTER PLOT SALVO: scatter_fob_tributos.png")
    plt.close()
    
    # 3. TOP 20 MAIS FODIDOS
    plt.figure(figsize=(12, 8))
    top_20 = df.nlargest(20, 'total_tributos')
    plt.barh([f"USD {x:,.0f}" for x in top_20['valor_fob_usd']], 
             top_20['total_tributos'], color='darkred')
    plt.title('TOP 20 OPERAÇÕES MAIS FODIDAS')
    plt.xlabel('Tributos (R$)')
    plt.tight_layout()
    plt.savefig('top_20_fodidos.png')
    print("✅ TOP 20 SALVO: top_20_fodidos.png")
    plt.close()
    
    # 4. GRÁFICO DE PIZZA DAS FAIXAS
    plt.figure(figsize=(8, 8))
    faixas = [
        (0, 500000, 'LEVE'),
        (500000, 1500000, 'MÉDIO'), 
        (1500000, 3000000, 'FODA'),
        (3000000, float('inf'), 'ARROMBADO')
    ]
    
    counts = []
    labels = []
    for min_val, max_val, cat in faixas:
        count = len([op for op in importacoes if min_val <= op['total_tributos'] < max_val])
        counts.append(count)
        labels.append(f'{cat}\n({count} ops)')
    
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('DISTRIBUIÇÃO DAS FODAS - 53.2% ARROMBADO!')
    plt.savefig('pie_distribuicao.png')
    print("✅ PIZZA SALVO: pie_distribuicao.png")
    plt.close()

def estatisticas_detalhadas():
    """NÚMEROS QUE VÃO FUDER SUA CABEÇA"""
    df = pd.DataFrame(importacoes)
    
    print("\n📈 ESTATÍSTICAS DETALHADAS:")
    print("=" * 40)
    
    print(f"💰 TRIBUTOS TOTAIS: R$ {df['total_tributos'].sum():,.2f}")
    print(f"📊 MÉDIA: R$ {df['total_tributos'].mean():,.2f}")
    print(f"📈 MÁXIMO: R$ {df['total_tributos'].max():,.2f}")
    print(f"📉 MÍNIMO: R$ {df['total_tributos'].min():,.2f}")
    print(f"📋 MEDIANA: R$ {df['total_tributos'].median():,.2f}")
    print(f"🎯 DESVIO PADRÃO: R$ {df['total_tributos'].std():,.2f}")
    
    # CORRELAÇÃO
    correlacao = df['valor_fob_usd'].corr(df['total_tributos'])
    print(f"🔗 CORRELAÇÃO FOB vs TRIBUTOS: {correlacao:.2f}")

if __name__ == "__main__":
    # PRIMEIRO EXECUTA AS SIMULAÇÕES
    from analise_simulacoes import foder_sistema_com_simulacoes
    foder_sistema_com_simulacoes(1000)
    
    # DEPOIS MOSTRA OS GRÁFICOS
    estatisticas_detalhadas()
    criar_graficos_arrombados()
    
    print("\n✅ TODOS OS GRÁFICOS SALVOS NA PASTA!")
    print("📁 ABRE OS PNGs PRA VER A FODA VISUALMENTE!")