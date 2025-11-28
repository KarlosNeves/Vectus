# empresas_avancado.py - SISTEMA DE CONSULTORIA TRIBUTÁRIA AVANÇADO
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from icms_importacao_rj import icms_importacao_rj

# 🎯 CONFIGURAÇÃO
import matplotlib
matplotlib.use('Agg')

# 🏢 BANCO DE DADOS COMPLETO DE EMPRESAS
empresas_avancado = {
    'TechGlobal Inc': {
        'cnpj': '12.345.678/0001-90', 'setor': 'Tecnologia', 'regime': 'Lucro Real',
        'porte': 'Grande', 'estado': 'SP', 'faturamento_anual': 500000000,
        'historico_importacoes': [], 'consultor_tributario': 'Dr. Silva'
    },
    'AutoParts BR': {
        'cnpj': '98.765.432/0001-10', 'setor': 'Automotivo', 'regime': 'Lucro Presumido', 
        'porte': 'Médio', 'estado': 'RJ', 'faturamento_anual': 150000000,
        'historico_importacoes': [], 'consultor_tributario': 'Dra. Santos'
    },
    'PharmaCorp LTDA': {
        'cnpj': '45.678.901/0001-23', 'setor': 'Farmacêutico', 'regime': 'Lucro Real',
        'porte': 'Grande', 'estado': 'SP', 'faturamento_anual': 800000000,
        'historico_importacoes': [], 'consultor_tributario': 'Dr. Costa'
    },
    'AgroFortaleza': {
        'cnpj': '34.567.890/0001-34', 'setor': 'Agronegócio', 'regime': 'Simples Nacional',
        'porte': 'Pequeno', 'estado': 'MT', 'faturamento_anual': 200000000,
        'historico_importacoes': [], 'consultor_tributario': 'Dra. Oliveira'
    },
    'VarejoMax': {
        'cnpj': '23.456.789/0001-45', 'setor': 'Varejo', 'regime': 'Lucro Presumido',
        'porte': 'Grande', 'estado': 'SP', 'faturamento_anual': 1200000000,
        'historico_importacoes': [], 'consultor_tributario': 'Dr. Rodrigues'
    },
    'QuimicaBrasil': {
        'cnpj': '56.789.012/0001-56', 'setor': 'Química', 'regime': 'Lucro Real',
        'porte': 'Médio', 'estado': 'RS', 'faturamento_anual': 300000000,
        'historico_importacoes': [], 'consultor_tributario': 'Dra. Fernandes'
    }
}

# 📦 PRODUTOS DETALHADOS POR SETOR
produtos_detalhados = {
    'Tecnologia': {
        'Notebooks Gamer': (1500, 5000), 'Servidores Rack': (10000, 50000),
        'Processadores': (500, 3000), 'Placas de Vídeo': (800, 4000),
        'SSDs NVMe': (300, 2000), 'Roteadores Enterprise': (2000, 15000)
    },
    'Automotivo': {
        'Motores 2.0 Turbo': (8000, 25000), 'Câmbios Automáticos': (5000, 20000),
        'Sistemas de Freio ABS': (2000, 8000), 'Baterias Elétricas': (3000, 15000),
        'Pneus High Performance': (500, 2000), 'Suspensão Esportiva': (3000, 12000)
    },
    'Farmacêutico': {
        'Equipamentos de Raio-X': (50000, 300000), 'Medicamentos Controlados': (1000, 50000),
        'Insumos Químicos': (5000, 50000), 'Máquinas de Laboratório': (20000, 200000),
        'Vacinas': (5000, 100000), 'Resonância Magnética': (100000, 800000)
    },
    'Agronegócio': {
        'Tratores Agrícolas': (80000, 300000), 'Colheitadeiras': (150000, 600000),
        'Fertilizantes': (5000, 50000), 'Sementes Geneticamente Modificadas': (10000, 80000),
        'Sistemas de Irrigação': (20000, 150000), 'Pivôs Centrais': (50000, 250000)
    },
    'Varejo': {
        'Eletrodomésticos Premium': (500, 5000), 'Smartphones': (300, 2000),
        'Roupas Importadas': (50, 500), 'Cosméticos Luxury': (100, 1000),
        'Bebidas Finas': (30, 300), 'Móveis Design': (1000, 10000)
    },
    'Química': {
        'Resinas Especiais': (5000, 50000), 'Petroquímicos': (10000, 100000),
        'Fertilizantes Nitrogenados': (8000, 80000), 'Polímeros': (3000, 30000),
        'Insumos Farmacêuticos': (10000, 150000), 'Catalisadores': (20000, 200000)
    }
}

def simular_importacao_inteligente(nome_empresa, num_operacoes=50):
    """
    🧠 SIMULAÇÃO INTELIGENTE COM DATAS E PADRÕES REALISTAS
    """
    empresa = empresas_avancado[nome_empresa]
    setor = empresa['setor']
    
    print(f"🚀 Simulando {num_operacoes} importações inteligentes para {nome_empresa}...")
    
    # 🎯 DATA INICIAL ALEATÓRIA (últimos 2 anos)
    data_base = datetime.now() - timedelta(days=730)
    
    for i in range(num_operacoes):
        # 🎯 PRODUTO E VALOR ESPECÍFICO
        produto = random.choice(list(produtos_detalhados[setor].keys()))
        min_val, max_val = produtos_detalhados[setor][produto]
        valor_fob = random.randint(min_val, max_val)
        
        # 🎯 DATA REALISTA (evita operações no mesmo dia)
        data_operacao = data_base + timedelta(days=random.randint(0, 730))
        
        # 🎯 CÂMBIO HISTÓRICO (variação realista)
        cambio = round(random.uniform(4.8, 6.2), 2)
        
        # 🎯 ALÍQUOTA INTELIGENTE (baseada em estado e porte)
        aliquota_base = 0.18
        if empresa['estado'] in ['SP', 'RJ']:
            aliquota_base += 0.01  # Estados com ICMS mais alto
        if empresa['porte'] == 'Grande':
            aliquota_base += 0.01  # Grandes empresas pagam mais
            
        aliquota_icms = round(aliquota_base + random.uniform(-0.01, 0.01), 2)
        
        # 🎯 CÁLCULO TRIBUTÁRIO
        resultado = icms_importacao_rj(valor_fob, cambio, aliquota_icms=aliquota_icms)
        
        # 🎯 OPERAÇÃO COMPLETA COM METADADOS
        operacao = {
            'id_operacao': f"{nome_empresa[:3].upper()}-{data_operacao.strftime('%Y%m%d')}-{i+1:03d}",
            'data_operacao': data_operacao.strftime('%Y-%m-%d'),
            'produto': produto,
            'valor_fob_usd': valor_fob,
            'cambio': cambio,
            'aliquota_icms': aliquota_icms,
            'setor': setor,
            'estado': empresa['estado'],
            'porte': empresa['porte'],
            'consultor': empresa['consultor_tributario'],
            **resultado
        }
        
        empresa['historico_importacoes'].append(operacao)

def analise_consultoria_tributaria():
    """
    💼 ANÁLISE DE CONSULTORIA PROFISSIONAL
    """
    print("\n💼 RELATÓRIO DE CONSULTORIA TRIBUTÁRIA - TRIBUTEC AI")
    print("=" * 70)
    
    # 📊 MÉTRICAS GLOBAIS
    total_operacoes = sum(len(emp['historico_importacoes']) for emp in empresas_avancado.values())
    total_tributos_geral = sum(
        sum(op['total_tributos'] for op in emp['historico_importacoes']) 
        for emp in empresas_avancado.values()
    )
    
    print(f"📈 RESUMO GERAL:")
    print(f"   🏢 Empresas Analisadas: {len(empresas_avancado)}")
    print(f"   📦 Total de Operações: {total_operacoes}")
    print(f"   💰 Tributos Totais: R$ {total_tributos_geral:,.2f}")
    print(f"   🏛️ ICMS Total: R$ {sum(sum(op['icms_devido'] for op in emp['historico_importacoes']) for emp in empresas_avancado.values()):,.2f}")
    
    # 🏆 RANKING DAS EMPRESAS
    print(f"\n🏆 RANKING POR TRIBUTAÇÃO TOTAL:")
    ranking = []
    for nome, dados in empresas_avancado.items():
        historico = dados['historico_importacoes']
        if historico:
            total_tributos = sum(op['total_tributos'] for op in historico)
            media_por_operacao = total_tributos / len(historico)
            ranking.append((nome, total_tributos, media_por_operacao, dados['setor']))
    
    # 🎯 ORDENA DO MAIOR PRO MENOR
    ranking.sort(key=lambda x: x[1], reverse=True)
    
    for i, (nome, total, media, setor) in enumerate(ranking, 1):
        medal = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣'][i-1]
        print(f"   {medal} {nome} ({setor}): R$ {total:,.2f} | Média: R$ {media:,.2f}/op")
    
    # 📊 ANÁLISE POR SETOR
    print(f"\n📊 ANÁLISE POR SETOR:")
    tributos_por_setor = {}
    for nome, dados in empresas_avancado.items():
        setor = dados['setor']
        historico = dados['historico_importacoes']
        if historico:
            total_setor = sum(op['total_tributos'] for op in historico)
            if setor not in tributos_por_setor:
                tributos_por_setor[setor] = 0
            tributos_por_setor[setor] += total_setor
    
    for setor, total in sorted(tributos_por_setor.items(), key=lambda x: x[1], reverse=True):
        print(f"   📈 {setor}: R$ {total:,.2f}")

def identificar_oportunidades_otimizacao():
    """
    🔍 IDENTIFICA OPORTUNIDADES DE OTIMIZAÇÃO TRIBUTÁRIA
    """
    print(f"\n🔍 OPORTUNIDADES DE OTIMIZAÇÃO TRIBUTÁRIA")
    print("=" * 60)
    
    for nome, dados in empresas_avancado.items():
        historico = dados['historico_importacoes']
        if not historico:
            continue
            
        # 🎯 CALCULA EFICIÊNCIA TRIBUTÁRIA
        total_tributos = sum(op['total_tributos'] for op in historico)
        total_valor_brl = sum(op['valor_brl'] for op in historico)
        eficiencia_tributaria = (total_tributos / total_valor_brl) * 100
        
        # 🎯 ENCONTRA OPERAÇÕES MAIS CARAS
        operacoes_caras = sorted(historico, key=lambda x: x['total_tributos'], reverse=True)[:3]
        
        print(f"\n🏢 {nome} ({dados['setor']}) - Consultor: {dados['consultor_tributario']}")
        print(f"   📊 Eficiência Tributária: {eficiencia_tributaria:.1f}%")
        
        if eficiencia_tributaria > 60:
            print(f"   ⚠️  ALERTA: Eficiência tributária acima do ideal!")
            print(f"   💡 SUGESTÃO: Revisar estratégia de importação")
        
        print(f"   🎯 TOP 3 OPERAÇÕES MAIS TRIBUTADAS:")
        for i, op in enumerate(operacoes_caras, 1):
            print(f"      {i}. {op['produto']} - R$ {op['total_tributos']:,.2f}")

def criar_dashboard_avancado():
    """
    📈 DASHBOARD AVANÇADO COM MÚLTIPLOS GRÁFICOS
    """
    print(f"\n🎨 Criando dashboard avançado...")
    
    # 📊 PREPARA DADOS
    dados_graficos = []
    for nome, dados in empresas_avancado.items():
        historico = dados['historico_importacoes']
        if historico:
            total_tributos = sum(op['total_tributos'] for op in historico)
            total_icms = sum(op['icms_devido'] for op in historico)
            eficiencia = (total_tributos / sum(op['valor_brl'] for op in historico)) * 100
            
            dados_graficos.append({
                'empresa': nome,
                'setor': dados['setor'],
                'total_tributos': total_tributos,
                'total_icms': total_icms,
                'eficiencia': eficiencia,
                'porte': dados['porte'],
                'consultor': dados['consultor_tributario']
            })
    
    df = pd.DataFrame(dados_graficos)
    
    # 1. 📊 GRÁFICO DE BARRAS - TRIBUTAÇÃO POR SETOR
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    setor_tributos = df.groupby('setor')['total_tributos'].sum()
    bars = plt.bar(setor_tributos.index, setor_tributos.values, color=plt.cm.Set3(range(len(setor_tributos))))
    plt.title('TRIBUTAÇÃO TOTAL POR SETOR', fontweight='bold', fontsize=12)
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, f'R$ {height:,.0f}', 
                ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # 2. 📈 GRÁFICO DE DISPERSÃO - EFICIÊNCIA vs TRIBUTAÇÃO
    plt.subplot(2, 2, 2)
    colors = {'Grande': 'red', 'Médio': 'blue', 'Pequeno': 'green'}
    
    for porte, color in colors.items():
        mask = df['porte'] == porte
        plt.scatter(df[mask]['eficiencia'], df[mask]['total_tributos']/1e6, 
                   c=color, label=porte, s=100, alpha=0.7)
    
    plt.xlabel('Eficiência Tributária (%)')
    plt.ylabel('Tributos Totais (Milhões R$)')
    plt.title('EFICIÊNCIA vs TRIBUTAÇÃO', fontweight='bold', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 3. 🥧 GRÁFICO DE PIZZA - DISTRIBUIÇÃO POR CONSULTOR
    plt.subplot(2, 2, 3)
    consultor_tributos = df.groupby('consultor')['total_tributos'].sum()
    plt.pie(consultor_tributos.values, labels=consultor_tributos.index, autopct='%1.1f%%')
    plt.title('DISTRIBUIÇÃO POR CONSULTOR', fontweight='bold', fontsize=12)
    
    # 4. 📋 GRÁFICO DE BARRAS HORIZONTAIS - TOP EMPRESAS
    plt.subplot(2, 2, 4)
    top_empresas = df.nlargest(5, 'total_tributos')
    plt.barh(top_empresas['empresa'], top_empresas['total_tributos']/1e6, color='darkred')
    plt.xlabel('Tributos Totais (Milhões R$)')
    plt.title('TOP 5 EMPRESAS MAIS TRIBUTADAS', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('dashboard_consultoria_tributaria.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Dashboard salvo: 'dashboard_consultoria_tributaria.png'")

def gerar_relatorio_executivo():
    """
    📄 RELATÓRIO EXECUTIVO COMPLETO EM CSV
    """
    print(f"\n💾 Gerando relatório executivo...")
    
    # 📊 COMPILA TODOS OS DADOS
    todos_dados = []
    metricas_empresas = []
    
    for nome, dados in empresas_avancado.items():
        historico = dados['historico_importacoes']
        
        if historico:
            # 🎯 DADOS DETALHADOS
            for operacao in historico:
                todos_dados.append({
                    'empresa': nome,
                    'setor': dados['setor'],
                    'porte': dados['porte'],
                    'estado': dados['estado'],
                    'regime_tributario': dados['regime'],
                    'consultor': dados['consultor_tributario'],
                    'faturamento_anual': dados['faturamento_anual'],
                    **operacao
                })
            
            # 🎯 MÉTRICAS CONSOLIDADAS
            total_tributos = sum(op['total_tributos'] for op in historico)
            total_icms = sum(op['icms_devido'] for op in historico)
            eficiencia = (total_tributos / sum(op['valor_brl'] for op in historico)) * 100
            
            metricas_empresas.append({
                'empresa': nome,
                'setor': dados['setor'],
                'porte': dados['porte'],
                'consultor': dados['consultor_tributario'],
                'total_operacoes': len(historico),
                'total_tributos': total_tributos,
                'total_icms': total_icms,
                'eficiencia_tributaria': eficiencia,
                'tributos_por_operacao': total_tributos / len(historico)
            })
    
    # 💾 EXPORTA OS DADOS
    pd.DataFrame(todos_dados).to_csv('dados_detalhados_consultoria.csv', index=False, encoding='utf-8')
    pd.DataFrame(metricas_empresas).to_csv('metricas_empresas_consultoria.csv', index=False, encoding='utf-8')
    
    print("✅ Relatórios exportados:")
    print("   - 'dados_detalhados_consultoria.csv' (dados completos)")
    print("   - 'metricas_empresas_consultoria.csv' (métricas consolidadas)")

# 🚀 EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    print("🚀 SISTEMA AVANÇADO DE CONSULTORIA TRIBUTÁRIA - TRIBUTEC AI")
    print("=" * 70)
    
    # 1. 🧠 SIMULAÇÃO INTELIGENTE
    for empresa in empresas_avancado.keys():
        simular_importacao_inteligente(empresa, 40)  # 40 operações por empresa
    
    # 2. 💼 ANÁLISE DE CONSULTORIA
    analise_consultoria_tributaria()
    
    # 3. 🔍 IDENTIFICAÇÃO DE OPORTUNIDADES
    identificar_oportunidades_otimizacao()
    
    # 4. 📈 DASHBOARD AVANÇADO
    criar_dashboard_avancado()
    
    # 5. 📄 RELATÓRIO EXECUTIVO
    gerar_relatorio_executivo()
    
    # 🎯 RESUMO FINAL
    total_ops = sum(len(emp['historico_importacoes']) for emp in empresas_avancado.values())
    print(f"\n🎊 CONSULTORIA TRIBUTÁRIA CONCLUÍDA!")
    print(f"📈 {total_ops} operações analisadas")
    print(f"🏢 {len(empresas_avancado)} empresas consultadas")
    print(f"💼 {len(set(emp['consultor_tributario'] for emp in empresas_avancado.values()))} consultores envolvidos")
    print(f"📊 1 dashboard profissional gerado")
    print(f"📄 2 relatórios executivos exportados")
    print(f"\n🔥 PRÓXIMA FASE: ANÁLISE DOS RELATÓRIOS E DASHBOARD!")