
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)

CORS(app)



load_dotenv()

file_path = '../../../Desktop/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf'
loader = PyPDFLoader(file_path)
docs = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
 chunk_size=2000,
    chunk_overlap=100,
    )

texts = text_splitter.split_documents(docs)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


vector_store = Chroma(
    collection_name="RAG-2",
    embedding_function=embeddings
)

documents = [
    {
        "pageContent": text,
        "metadata": {
            "id": str(index),          
            "chunkIndex": index        }
    }
    for index, text in enumerate(texts)
]


vector_store.add_documents(documents=texts)

retriever= vector_store.as_retriever(
    search_kwargs={"k": 2},
    search_type="similarity",
    search_score=True,
)

llm =  ChatGoogleGenerativeAI(
            model= "gemini-1.5-pro",
            temperature= 0.2,
            max_retries= 2,
        );


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

@app.route("/")
def index():
    return "Hello, World!"


@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('message', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    retrievedDocs = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in retrievedDocs)
    prompt_value = template.invoke({
        "query": query,
        "context": context
    })
            

    answer = llm.invoke(prompt_value)
    return jsonify({"answer": answer.content})



if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5328)

