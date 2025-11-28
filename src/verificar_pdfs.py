import os
from pathlib import Path
from PyPDF2 import PdfReader

# Caminho da pasta de PDFs
DATA_DIR = Path("c:/Users/Edcarlos/Desktop/cip_works/tributec-ai/data/exatas_logica")

print("🔍 Verificando integridade dos PDFs...\n")

for pdf in DATA_DIR.glob("*.pdf"):
    try:
        reader = PdfReader(str(pdf))
        num_pages = len(reader.pages)
        print(f"✅ {pdf.name} - {num_pages} páginas")
        
        # Testa extrair texto da primeira página
        page = reader.pages[0]
        text = page.extract_text()
        if not text or len(text) < 50:
            print(f"   ⚠️  AVISO: Texto muito curto ou vazio na primeira página")
            
    except Exception as e:
        print(f"❌ {pdf.name} - CORROMPIDO: {e}")
        print(f"   → Baixe uma nova versão desse arquivo.\n")

print("\n✔️ Verificação concluída!")