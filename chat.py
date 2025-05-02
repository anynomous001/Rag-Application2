from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Update CORS configuration for production
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend-domain.onrender.com", "http://localhost:3000"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Load environment variables
load_dotenv()

# Verify Google API key is set
if not os.getenv('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY environment variable is not set!")

try:
    logger.info("Loading PDF file...")
    file_path = './Nadia Makarevich - Advanced React_ deep dives, investigations, performance patterns and techniques-anonymous (2023).pdf'
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    logger.info("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100,
    )

    texts = text_splitter.split_documents(docs)

    logger.info("Initializing embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    logger.info("Setting up Qdrant client...")
    client = QdrantClient(":memory:")

    logger.info("Creating collection...")
    client.create_collection(
        collection_name="RAG-2",
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        ),
    )

    logger.info("Creating vector store...")
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="RAG-2",
        embedding=embeddings,
    )

    logger.info("Adding documents to vector store...")
    vector_store.add_documents(documents=texts)

    logger.info("Setting up retriever...")
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 2},
        search_type="similarity",
        search_score=True,
    )

    logger.info("Initializing LLM...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.2,
        max_retries=2,
    )

    template = ChatPromptTemplate([
        ("system", """You are a helpful assistant. Your Name is Cal.
         Answer ONLY from the provided document {context}.
        If the {context} is insufficient, just say you do not know."""),
        ("human", "what is happiness?"),
        ("ai", """According to The Almanack of Naval Ravikant, happiness is not something to be pursued—it is your natural state when you remove suffering. Naval says, “A happy person isn’t someone who’s happy all the time—it’s someone who effortlessly interprets events in such a way that they don’t lose their innate peace.” He explains that desire is a contract you make with yourself to be unhappy until you get what you want.
        In his words, “A rational person can find peace by cultivating indifference to things outside of their control.” He urges us to escape the trap of endless desire and comparison, saying, “Play stupid games, win stupid prizes.” Instead, Naval suggests practicing meditation, self-inquiry, and stillness. “Happiness is a choice you make and a skill you develop. You choose to be happy, and then you work at it. It’s just like building muscles.”
        Ultimately, Naval’s philosophy is simple: happiness is found not in achieving more, but in needing less."""),
        ("human", "{query}"),
    ])

except Exception as e:
    logger.error(f"An error occurred during initialization: {str(e)}")
    raise

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get('message', '')
        if not query:
            return jsonify({"error": "No query provided"}), 400

        logger.info(f"Processing query: {query}")
        retrievedDocs = retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in retrievedDocs)
        
        prompt_value = template.invoke({
            "query": query,
            "context": context
        })
                
        answer = llm.invoke(prompt_value)
        return jsonify({"answer": answer.content})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable for Render compatibility
    port = int(os.environ.get('PORT', 5328))
    
    logger.info(f"Starting server on port {port}...")
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)

