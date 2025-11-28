# src/create_index.py
import os
import glob
from pathlib import Path
from python_dotenv import load_dotenv

from langchain.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Carregar variáveis de ambiente (.env)
load_dotenv()

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent  # tributec-ai/
DATA_DIR = PROJECT_ROOT / "data"
INDEX_DIR = PROJECT_ROOT / "index"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Criar pastas
INDEX_DIR.mkdir(exist_ok=True)

print("Carregando documentos de 'data/'...")

documents = []

# --- TXT ---
for file_path in DATA_DIR.glob("*.txt"):
    print(f"  TXT: {file_path.name}")
    loader = TextLoader(file_path, encoding="utf-8")
    documents.extend(loader.load())

# --- PDF ---
for file_path in DATA_DIR.glob("*.pdf"):
    print(f"  PDF: {file_path.name}")
    loader = PyPDFLoader(str(file_path))
    documents.extend(loader.load())

# --- CSV ---
for file_path in DATA_DIR.glob("*.csv"):
    print(f"  CSV: {file_path.name}")
    loader = CSVLoader(str(file_path))
    documents.extend(loader.load())

if not documents:
    print("Nenhum arquivo .txt, .pdf ou .csv encontrado em data/!")
    exit()

print(f"Total de páginas/documentos carregados: {len(documents)}")

# Dividir em chunks
print("Dividindo em chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
)
chunks = splitter.split_documents(documents)
print(f"Total de chunks: {len(chunks)}")

# Criar índice FAISS
print("Gerando embeddings e salvando índice...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = FAISS.from_documents(chunks, embeddings)
db.save_local(INDEX_DIR)

print(f"\nÍNDICE CRIADO COM SUCESSO!")
print(f"Local: {INDEX_DIR}")
print(f"Pronto para perguntas com query_rag.py!")