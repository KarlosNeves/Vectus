# src/query_rag.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Carregar .env
load_dotenv()

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent
INDEX_DIR = PROJECT_ROOT / "index"

# Verificar se o índice existe
if not INDEX_DIR.exists():
    print("Erro: Índice não encontrado!")
    print("Rode primeiro: python src/create_index.py")
    sys.exit(1)

print("Carregando índice FAISS...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)

# Configurar o modelo de resposta
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Criar pipeline RAG
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True
)

def perguntar(pergunta):
    print(f"\nPergunta: {pergunta}")
    print("-" * 50)
    result = qa({"query": pergunta})
    print(f"Resposta: {result['result']}")
    print("-" * 50)
    print("Fontes usadas:")
    for i, doc in enumerate(result["source_documents"], 1):
        fonte = doc.metadata.get("source", "desconhecida")
        pagina = doc.metadata.get("page", "N/A")
        print(f"  {i}. {fonte} (pág. {pagina})")

# === EXECUÇÃO ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/query_rag.py \"Sua pergunta aqui\"")
        print("\nExemplo:")
        print('   python src/query_rag.py "Qual é o prazo final do projeto?"')
        sys.exit(1)

    pergunta = " ".join(sys.argv[1:])
    perguntar(pergunta)