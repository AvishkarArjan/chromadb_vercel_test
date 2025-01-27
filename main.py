from dotenv import load_dotenv
load_dotenv()
import os
from pprint import pprint
print("Started")
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

HF_API_KEY = os.getenv("HF_API_KEY")
embed_model = os.getenv("EMBED_MODEL")
source = "./reliance_report.pdf"
file_id = 1

print(embed_model)
print(source)

embeddings = HuggingFaceInferenceAPIEmbeddings(
    model_name=embed_model,
    api_key=HF_API_KEY
)



# Load and split the document
loader = PyPDFLoader(source)
documents = loader.load()

# Split text into smaller chunks for better indexing
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Define chunk size
    chunk_overlap=50  # Define overlap between chunks for better context
)
chunks = text_splitter.split_documents(documents)
if not chunks:
    raise ValueError("No chunks created. Check the document loader or splitter settings.")


# Initialize Chroma vector database
chroma_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Add documents to the Chroma database
chroma_db.add_documents(chunks)

# Persist the database for later use
# chroma_db.persist()

print("Document indexed into Chroma vector database.")

retriever =chroma_db.as_retriever(search_kwargs={"k": 2})
pprint(retriever.invoke("products and services"))
# retriever = get_retriever()
# retrieved_docs = retriever.invoke("products and services")
# content = "\n".join([doc.page_content for doc in retrieved_docs])
# pprint(content)

# pprint(load_pdf(source))

