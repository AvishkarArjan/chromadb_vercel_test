from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pprint import pprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize embeddings
HF_API_KEY = os.getenv("HF_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL")
EMBEDDINGS = HuggingFaceInferenceAPIEmbeddings(
    model_name=EMBED_MODEL,
    api_key=HF_API_KEY
)

# Initialize Chroma DB
CHROMA_DB = Chroma(persist_directory="./chroma_db", embedding_function=EMBEDDINGS)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Chroma DB Flask API!"})

@app.route("/index-document", methods=["POST"])
def index_document():
    try:
        # Get the file and metadata from the request
        file = request.files.get("file")
        share_name = request.form.get("share_name")
        date = request.form.get("date")

        if not file or not share_name or not date:
            return jsonify({"error": "File, share_name, and date are required."}), 400

        # Save the uploaded file temporarily
        file_path = f"./temp/{file.filename}"
        os.makedirs("./temp", exist_ok=True)
        file.save(file_path)

        # Load and process the document
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)

        # Add metadata and index the document
        for chunk in chunks:
            chunk.metadata["share_name"] = share_name
            chunk.metadata["date"] = date

        CHROMA_DB.add_documents(chunks)

        # Clean up temporary file
        os.remove(file_path)

        return jsonify({"message": "Document indexed successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["GET"])
def search():
    try:
        query = request.args.get("query")
        share_name = request.args.get("share_name")
        k = int(request.args.get("k", 5))  # Default to top 5 results

        if not query:
            return jsonify({"error": "Query is required."}), 400

        # Search in Chroma DB with filters
        search_results = CHROMA_DB.similarity_search(
                query=query,
                k=k,
                filter={"share_name": share_name} if share_name else {}
            )
        # Sort results by date if metadata exists
        results = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in search_results
        ]
        sorted_results = sorted(
            results,
            key=lambda doc: doc["metadata"].get("date", ""),
            reverse=True
        )

        return jsonify({"results": sorted_results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
