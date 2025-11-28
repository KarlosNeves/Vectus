# arquivo: analise_top_empresas.py
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

# DEFINIÇÃO DA FUNÇÃO NO TOPO
def calcular_ict(total_tributos, valor_fob_brl, benchmark=0.35):
    if valor_fob_brl == 0:
        return 0.0
    return round((total_tributos / valor_fob_brl) / benchmark, 3)

print("🎯 ANALISANDO TOP 5 EMPRESAS COM MAIOR POTENCIAL...")

# Carrega os dados
df_operacoes = pd.read_csv('./output/operacoes_reais_simuladas.csv')

# Seleciona as top 5 por capital social
top_5 = df_operacoes.nlargest(5, 'capital_social_real')

print(f"📊 TOP 5 EMPRESAS IDENTIFICADAS:")
for i, (_, emp) in enumerate(top_5.iterrows(), 1):
    print(f"   {i}. {emp['razao_social']} - R$ {emp['capital_social_real']:,.0f}")

# Análise detalhada das top 5
analise_detalhada = []

for _, empresa in top_5.iterrows():
    # Simula cenários de otimização
    carga_atual = empresa['total_tributos']
    
    # Cenário 1: Drawback (reduz II em 50%)
    ii_otimizado = empresa['valor_fob_brl'] * 0.01  # II de 2% para 1%
    carga_drawback = carga_atual - (empresa['valor_fob_brl'] * 0.01)
    
    # Cenário 2: Benefício ICMS (reduz ICMS em 30%)
    icms_otimizado = empresa['valor_fob_brl'] * 0.119  # ICMS médio de 17% para 11.9%
    carga_icms = carga_atual - (empresa['valor_fob_brl'] * 0.051)
    
    # Cenário 3: Otimização completa
    carga_otimizada = carga_atual * 0.7  # Redução de 30%
    
    analise = {
        'razao_social': empresa['razao_social'],
        'cnpj_basico': empresa['cnpj_basico'],
        'capital_social': empresa['capital_social_real'],
        'porte': empresa['porte_empresa'],
        'valor_fob_usd': empresa['valor_fob_usd'],
        'valor_fob_brl': empresa['valor_fob_brl'],
        'carga_atual': carga_atual,
        'ict_atual': empresa['ict'],
        # Cenários de otimização
        'economia_drawback': carga_atual - carga_drawback,
        'economia_icms': carga_atual - carga_icms,
        'economia_total': carga_atual - carga_otimizada,
        'carga_otimizada': carga_otimizada,
        'ict_otimizado': calcular_ict(carga_otimizada, empresa['valor_fob_brl'], 0.35)
    }
    analise_detalhada.append(analise)

# Cria DataFrame da análise
df_analise = pd.DataFrame(analise_detalhada)

# Gera relatório específico
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Análise Estratégica - Top 5 Empresas</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .empresa-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 5px solid #3498db;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        .metric {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        .economia {{
            background: #d4edda;
            border-left: 5px solid #28a745;
        }}
        .recomendacao {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        .destaque {{
            background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 ANÁLISE ESTRATÉGICA - TOP 5 EMPRESAS</h1>
            <p>Foco em otimização tributária para empresas de alto potencial</p>
            <p><em>Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</em></p>
        </div>

        <div class="destaque">
            <h2>💰 POTENCIAL DE ECONOMIA IDENTIFICADO</h2>
            <p>Análise de cenários de otimização para as 5 empresas com maior capital social</p>
        </div>
"""

# Adiciona análise de cada empresa
for i, emp in df_analise.iterrows():
    html_content += f"""
        <div class="empresa-card">
            <h3>🏢 {emp['razao_social']}</h3>
            <p><strong>CNPJ Básico:</strong> {emp['cnpj_basico']} | <strong>Porte:</strong> {emp['porte']} | <strong>Capital Social:</strong> R$ {emp['capital_social']:,.0f}</p>
            
            <div class="metric-grid">
                <div class="metric">
                    <div class="metric-value">R$ {emp['valor_fob_brl']:,.0f}</div>
                    <div class="metric-label">Valor FOB (R$)</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{emp['ict_atual']:.2f}</div>
                    <div class="metric-label">ICT Atual</div>
                </div>
                <div class="metric">
                    <div class="metric-value">R$ {emp['carga_atual']:,.0f}</div>
                    <div class="metric-label">Carga Tributária</div>
                </div>
            </div>

            <div class="recomendacao">
                <h4>🎯 CENÁRIOS DE OTIMIZAÇÃO:</h4>
                <div class="metric-grid">
                    <div class="metric economia">
                        <div class="metric-value">R$ {emp['economia_drawback']:,.0f}</div>
                        <div class="metric-label">Drawback (II)</div>
                    </div>
                    <div class="metric economia">
                        <div class="metric-value">R$ {emp['economia_icms']:,.0f}</div>
                        <div class="metric-label">Benefício ICMS</div>
                    </div>
                    <div class="metric economia">
                        <div class="metric-value">R$ {emp['economia_total']:,.0f}</div>
                        <div class="metric-label">Otimização Total</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{emp['ict_otimizado']:.2f}</div>
                        <div class="metric-label">ICT Otimizado</div>
                    </div>
                </div>
            </div>

            <div class="recomendacao">
                <h4>📋 RECOMENDAÇÕES ESPECÍFICAS:</h4>
"""

    # Recomendações personalizadas por empresa
    if emp['capital_social'] > 5000000:
        html_content += f"""
                <p>✅ <strong>HOLDING</strong> - Estruturação societária para otimização</p>
                <p>✅ <strong>DRAWBACK</strong> - Isenção de II e IPI para importações</p>
                <p>✅ <strong>CONVÊNIOS ICMS</strong> - Negociação interestadual</p>
                <p>✅ <strong>REGRIME TRIBUTÁRIO</strong> - Lucro Real com planejamento</p>
"""
    elif emp['capital_social'] > 1000000:
        html_content += f"""
                <p>✅ <strong>REGIME TRIBUTÁRIO</strong> - Revisão Lucro Real vs Presumido</p>
                <p>✅ <strong>BENEFÍCIOS FISCAIS</strong> - Incentivos setoriais</p>
                <p>✅ <strong>PLANEJAMENTO</strong> - Estratégia de desembaraço</p>
                <p>✅ <strong>CRÉDITOS FISCAIS</strong> - Aproveitamento de PIS/COFINS</p>
"""
    else:
        html_content += f"""
                <p>✅ <strong>SIMPLES NACIONAL</strong> - Verificar elegibilidade</p>
                <p>✅ <strong>CRÉDITOS FISCAIS</strong> - Aproveitamento de PIS/COFINS</p>
                <p>✅ <strong>CONSULTORIA</strong> - Análise específica do negócio</p>
                <p>✅ <strong>DOCUMENTAÇÃO</strong> - Regularização fiscal</p>
"""

    html_content += f"""
            </div>
        </div>
"""

# Resumo executivo
total_economia = df_analise['economia_total'].sum()
html_content += f"""
        <div class="empresa-card" style="background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%); color: white;">
            <h2>💰 RESUMO EXECUTIVO</h2>
            <div class="metric-grid">
                <div class="metric" style="background: rgba(255,255,255,0.2);">
                    <div class="metric-value" style="color: white;">R$ {total_economia:,.0f}</div>
                    <div class="metric-label" style="color: white;">ECONOMIA TOTAL POTENCIAL</div>
                </div>
                <div class="metric" style="background: rgba(255,255,255,0.2);">
                    <div class="metric-value" style="color: white;">5</div>
                    <div class="metric-label" style="color: white;">EMPRESAS ANALISADAS</div>
                </div>
                <div class="metric" style="background: rgba(255,255,255,0.2);">
                    <div class="metric-value" style="color: white;">{df_analise['ict_otimizado'].mean():.2f}</div>
                    <div class="metric-label" style="color: white;">ICT MÉDIO OTIMIZADO</div>
                </div>
            </div>
        </div>

        <div class="recomendacao">
            <h3>🚀 PRÓXIMOS PASSOS RECOMENDADOS:</h3>
            <p>1. <strong>Contatar ICO.N HOLDING</strong> - Maior potencial (R$ {df_analise.iloc[0]['economia_total']:,.0f})</p>
            <p>2. <strong>Estudo de Drawback</strong> - Para empresas acima de R$ 1 milhão</p>
            <p>3. <strong>Análise de regime tributário</strong> - Otimização legal</p>
            <p>4. <strong>Consultoria especializada</strong> - Implementação das estratégias</p>
            <p>5. <strong>Monitoramento contínuo</strong> - Acompanhamento dos resultados</p>
        </div>

        <footer style="text-align: center; margin-top: 40px; color: #666; padding: 20px;">
            <p><strong>Tributec v2.0</strong> - Análise Estratégica de Alto Impacto</p>
            <p>"Foco nas oportunidades reais, não nos problemas imaginários"</p>
        </footer>
    </div>
</body>
</html>
"""

# Salva o relatório
with open('./output/analise_top_empresas.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Salva CSV com análise detalhada
df_analise.to_csv('./output/detalhes_top_empresas.csv', index=False)

print("✅ ANÁLISE DAS TOP 5 EMPRESAS CONCLUÍDA!")
print("📁 Arquivos gerados:")
print("   - ./output/analise_top_empresas.html")
print("   - ./output/detalhes_top_empresas.csv")
print(f"💰 Economia total potencial: R$ {total_economia:,.0f}")
print("\n🎯 ABRA A ANÁLISE:")
print("   start ./output/analise_top_empresas.html")