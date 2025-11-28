# Arquivo: portfolio.py
import numpy as np

def calcular_mvp(varA, varB, covAB):
    """
    Calcula a ponderação ótima do Ativo A (wA) para o Portfólio de Mínima Variância (MVP).
    A função é vetorizada.
    """
    numerador = varB - covAB
    denominador = varA + varB - 2 * covAB
    return numerador / denominador