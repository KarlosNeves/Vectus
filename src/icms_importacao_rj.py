importacoes = []  # LISTA PRINCIPAL - ADICIONE AQUI!

def icms_importacao_rj(
    valor_fob_usd,
    cambio,
    aliquota_icms=0.18,
    ii_percent=0.60,
    ipi_percent=0.10,
    iof_cambio_percent=0.0038,  # IOF câmbio: 0,38%
    despesas_aduaneiras=0.0     # Taxas de despachante, armazenagem, etc.
):
    """
    Calcula ICMS de importação para o RJ conforme Lei 2.657/96.
    
    Base de cálculo inclui:
    - Valor FOB convertido
    - II
    - IPI
    - IOF Câmbio
    - Despesas aduaneiras
    - ICMS (cálculo por dentro)
    
    Exemplo:
    >>> icms_importacao_rj(100000, 5.60)
    {'icms_devido': 218456.0, 'total_tributos': 644456.0}
    """
    global importacoes  # 🔥 ADICIONE ESTA LINHA!
    
    # 1. Valor em reais
    valor_brl = round(valor_fob_usd * cambio, 2)
    
    # 2. IOF Câmbio (0,38% sobre o valor em reais)
    iof_cambio = round(valor_brl * iof_cambio_percent, 2)
    
    # 3. II (60% sobre valor FOB convertido)
    ii_valor = round(valor_brl * ii_percent, 2)
    
    # 4. Base para IPI (valor + II + IOF + despesas)
    base_ipi = valor_brl + ii_valor + iof_cambio + despesas_aduaneiras
    ipi_valor = round(base_ipi * ipi_percent, 2)
    
    # 5. Base do ICMS SEM o ICMS próprio
    base_icms_sem_icms = (
        valor_brl +
        ii_valor +
        ipi_valor +
        iof_cambio +
        despesas_aduaneiras
    )
    
    # 6. ICMS com cálculo por dentro
    icms_devido = round(
        base_icms_sem_icms * aliquota_icms / (1 - aliquota_icms), 2
    )
    
    # 7. Total de tributos
    total_tributos = ii_valor + ipi_valor + icms_devido + iof_cambio + despesas_aduaneiras

    # 🔥 ADICIONE ESTE BLOCO ANTES DO RETURN!
    registro = {
        'valor_fob_usd': valor_fob_usd,
        'cambio': cambio,
        'valor_brl': valor_brl,
        'ii_valor': ii_valor,
        'ipi_valor': ipi_valor,
        'icms_devido': icms_devido,
        'total_tributos': total_tributos,
        'aliquota_icms': aliquota_icms
    }
    importacoes.append(registro)  # ADICIONA À LISTA
    
    return {
        'valor_brl': valor_brl,
        'iof_cambio': iof_cambio,
        'ii_valor': ii_valor,
        'ipi_valor': ipi_valor,
        'despesas_aduaneiras': despesas_aduaneiras,
        'base_icms_sem_icms': base_icms_sem_icms,
        'icms_devido': icms_devido,
        'total_tributos': total_tributos
    }

# No final do icms_importacao_rj.py, adicione:
if __name__ == "__main__":
    print("🚀 Módulo ICMS Importação RJ carregado com sucesso!")
    
    # Teste rápido
    resultado = icms_importacao_rj(100000, 5.60)
    print("📊 Resultado:", resultado)
    print(f"📁 Registros na lista: {len(importacoes)}")
    if importacoes:
        print("📋 Último registro:", importacoes[-1])