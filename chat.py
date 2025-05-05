from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend-domain.onrender.com", "http://localhost:3000"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

load_dotenv()

if not os.getenv('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY environment variable is not set!")

try:
    vector_store = None
    retriever = None

    logger.info("Initializing embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    logger.info("Setting up Qdrant client...")
    client = QdrantClient(":memory:")

    # logger.info("Creating collection...")
    # client.create_collection(
    #     collection_name="RAG-2",
    #     vectors_config=VectorParams(
    #         size=768,
    #         distance=Distance.COSINE
    #     ),
    # )

    # logger.info("Creating vector store...")
    # vector_store = QdrantVectorStore(
    #     client=client,
    #     collection_name="RAG-2",
    #     embedding=embeddings,
    # )

    # logger.info("Setting up retriever...")
    # retriever = vector_store.as_retriever(
    # search_kwargs={"k": 2},
    # search_type="similarity",
    # search_score=True,
    # )
          

    logger.info("Initializing LLM...")
    llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.2,
    max_retries=2,
    )

  
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf(file_path):
    global vector_store, retriever
    try:
        logger.info(f"Loading PDF file from {file_path}...")
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        logger.info("Splitting text...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
        )
        texts = text_splitter.split_documents(docs)
        
        logger.info("Adding documents to vector store...")
        logs = vector_store.add_documents(documents=texts)
        print(logs)

        logger.info("Creating vector store...")

        vector_store = QdrantVectorStore.from_documents(
        docs=texts,
        embeddings=embeddings,
        url=os.getenv("QDRANT_URL"),
        prefer_grpc=True,
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name="rag-{collection_name}",
        )

        print({vector_store})
        logger.info("Setting up retriever...")

        retriever = vector_store.as_retriever(
        search_kwargs={"k": 2},
        search_type="similarity",
        search_score=True,
        )


        logger.info("Retriever setup complete.")
        logger.info("Documents added to vector store successfully.")
#         logger.info("Added documents to vector store...")
#         logger.info("Adding documents to vector store...")
#         logs = vector_store.add_documents(documents=texts)
#         print(logs)
        os.remove(file_path)  # Remove the file after processing
        logger.info(f"File {file_path} processed and removed successfully.")

        return True

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return False

@app.route('/api/upload', methods=['POST'])
def upload_file():
    print('api called')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            print(filepath)
            
            if process_pdf(filepath):
                return jsonify({'message': 'File successfully uploaded and processed'}), 200
            else:
                return jsonify({'error': 'Error processing the PDF'}), 500
                
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5328))
    
    logger.info(f"Starting server on port {port}...")
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)

