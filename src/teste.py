from collections import Counter

def verificar_anagrama(palavra1, palavra2):
    """
    Verifica se duas palavras são anagramas (possuem as mesmas letras na 
    mesma quantidade, ignorando espaços e diferenças de caixa/case).
    """
    # 1. Limpar e Padronizar as palavras
    # Remove espaços e converte para minúsculas
    p1_limpa = palavra1.replace(' ', '').lower()
    p2_limpa = palavra2.replace(' ', '').lower()

    # 2. Verificar se as contagens de caracteres são idênticas
    # Anagramas devem ter exatamente a mesma contagem de letras.
    # Counter cria um dicionário onde as chaves são letras e os valores são as contagens.
    return Counter(p1_limpa) == Counter(p2_limpa)

# --- Teste das Palavras ---

palavra_a = 'roma'
palavra_b = 'amor'
palavra_c = 'Mora'
palavra_d = 'mara'

# Teste 1: Anagramas básicos
resultado_1 = verificar_anagrama(palavra_a, palavra_b)
print(f"'{palavra_a}' e '{palavra_b}' são anagramas? {resultado_1}")

# Teste 2: Anagramas com diferença de caixa (case)
resultado_2 = verificar_anagrama(palavra_a, palavra_c)
print(f"'{palavra_a}' e '{palavra_c}' são anagramas? {resultado_2}")

# Teste 3: Não são anagramas
resultado_3 = verificar_anagrama(palavra_a, palavra_d)
print(f"'{palavra_a}' e '{palavra_d}' são anagramas? {resultado_3}")