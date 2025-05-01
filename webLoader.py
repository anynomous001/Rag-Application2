
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

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

def query_loop():
    print("Welcome to the RAG system. Type 'quit' to exit.\n")
    while True:
        try:
            query = input("\nEnter your question: ")
            if query.lower() == 'quit':
                print("Exiting...")
                break
            if not query.strip():
                continue
                
            # Process query
            docs = retriever.invoke(query)
            
            # Display results
            print(f"\nResults for: '{query}'")
            for i, result in enumerate(docs, 1):
                print(f"\n{'='*40} Result {i} {'='*40}")
                print(f"Page {result.metadata.get('page', 'N/A')}")
                print(f"\n{result.page_content}\n")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    query_loop()
    
