import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------
load_dotenv()

DATA_FOLDER = "data"
VECTOR_DB = "vectorstore"

print("=" * 60)
print("📚 Academic Notes Chatbot")
print("=" * 60)

# --------------------------------------------------
# Read PDFs
# --------------------------------------------------

documents = []

pdf_files = [
    file for file in os.listdir(DATA_FOLDER)
    if file.lower().endswith(".pdf")
]

if len(pdf_files) == 0:
    print("❌ No PDF files found inside the data folder.")
    exit()

print(f"\n📄 Found {len(pdf_files)} PDF files.\n")

for pdf in pdf_files:

    path = os.path.join(DATA_FOLDER, pdf)

    print(f"📥 Loading: {pdf}")

    loader = PyPDFLoader(path)

    docs = loader.load()

    documents.extend(docs)

print("\n✅ PDF Loading Completed")
print(f"Total Pages Loaded : {len(documents)}")

# --------------------------------------------------
# Split Documents
# --------------------------------------------------

print("\n✂ Splitting documents into chunks...")

text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=700,
    chunk_overlap=100,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

chunks = text_splitter.split_documents(documents)

print(f"✅ Total Chunks Created : {len(chunks)}")

# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

print("\n🧠 Loading Sentence Transformer...")

embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2",

    model_kwargs={
        "device": "cpu"
    },

    encode_kwargs={
        "normalize_embeddings": True
    }

)

print("✅ Embedding Model Loaded")

# --------------------------------------------------
# Create FAISS Vector Database
# --------------------------------------------------

print("\n📦 Creating FAISS Vector Database...")

vectorstore = FAISS.from_documents(

    documents=chunks,

    embedding=embeddings

)

vectorstore.save_local(VECTOR_DB)

print("\n" + "=" * 60)
print("🎉 SUCCESS!")
print("FAISS Vector Database Created Successfully")
print("=" * 60)

print(f"\n📁 Saved to : {VECTOR_DB}")
print(f"📄 PDFs     : {len(pdf_files)}")
print(f"📃 Pages    : {len(documents)}")
print(f"🧩 Chunks   : {len(chunks)}")