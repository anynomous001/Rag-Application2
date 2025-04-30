
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
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
            "id": str(index),           # Convert index to string
            "chunkIndex": index,
        }
    }
    for index, text in enumerate(texts)
]


vector_store.add_documents(documents=texts)

retriever= vector_store.as_retriever(
    search_kwargs={"k": 5},
    search_type="similarity",
    search_score=True,
)
query = "how to get rich?"
docs = retriever.invoke(query)


for result in docs:
    print(result)