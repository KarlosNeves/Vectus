# test_icms.py
from src.icms_rj import icms_importacao_rj

if __name__ == "__main__":
    print("TRIBUTEC-AI — TESTE ICMS RJ (Lei 2.657/96)")
    print("="*50)
    
    resultado = icms_importacao_rj(
        valor_fob_usd=100000,
        cambio=5.60,
        despesas_aduaneiras=5000
    )
    
    for k, v in resultado.items():
        print(f"{k:20}: R$ {v:,.2f}")