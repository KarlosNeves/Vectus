import numpy as np
import pytest

# A função calcular_mvp deve ser importada do arquivo portfolio.py
from portfolio import calcular_mvp 

def test_mvp_validacao_covariancia_zero():
    """
    TESTE CRÍTICO: Valida a ponderação do Ativo A (wA) quando a covariância (covAB) é zero.
    Cenário: varA=1, varB=4, covAB=0
    Cálculo esperado: wA = 4 / (1 + 4) = 0.8
    """
    # Dados de entrada (o Coder usou float para precisão, vamos seguir o padrão)
    varA = 1.0
    varB = 4.0
    covAB = 0.0

    # Resultado esperado
    wA_esperado = 0.8
    
    # Cálculo da ponderação usando a função MVP
    wA_calculado = calcular_mvp(varA, varB, covAB)

    # Asserção: Usa np.isclose (melhor prática) para garantir a precisão
    assert np.isclose(wA_calculado, wA_esperado), \
        f"Teste falhou! MVP com cov=0. Esperado: {wA_esperado}, Calculado: {wA_calculado}"

def test_mvp_caso_geral():
    """
    Teste um caso geral com covariância diferente de zero.
    Valores Exemplo (wA deve ser ~0.46)
    """
    varA = 0.010 # 10% de variância
    varB = 0.040 # 40% de variância
    covAB = 0.005 # Covariância de 0.5%
    
    # Cálculo manual do resultado esperado para este cenário
    # wA = (0.04 - 0.005) / (0.01 + 0.04 - 2 * 0.005) = 0.035 / 0.04 = 0.875
    wA_esperado = 0.875
    
    wA_calculado = calcular_mvp(varA, varB, covAB)

    assert np.isclose(wA_calculado, wA_esperado), \
        f"Teste falhou no caso geral. Esperado: {wA_esperado}, Calculado: {wA_calculado}"