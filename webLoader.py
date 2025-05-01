
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate



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
            retrievedDocs = retriever.invoke(query)

            context ="\n\n".join(doc.page_content for doc in retrievedDocs)

            
            prompt_value = template.invoke(
            {
                "query": query,
                "context": context
            }
           )
            

            answer = llm.invoke(prompt_value)
            
            
            # Display results
            # print(f"\nResults for: '{query}'")
            # for i, result in enumerate(docs, 1):
            #     print(f"\n{'='*40} Result {i} {'='*40}")
            #     print(f"Page {result.metadata.get('page', 'N/A')}")
            #     print(f"\n{result.page_content}\n")
            print(f"LLM Answer : {answer.content}")

#          [Document(metadata={'trapped': '/False', 'producer': 'macOS Version 10.15.5 (Build 19F101) Quartz PDFContext, AppendMode 1.1', 'page_label': '194', 'total_pages': 242, 'title': 'Eric-Jorgenson_The-Almanack-of-Naval-Ravikant.indd', 'gts_pdfxconformance': 'PDF/X-1a:2001', 'page': 193, 'source': '../../../Desktop/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf', 'creator': 'Adobe InDesign 15.1 
# (Macintosh)', 'creationdate': '2020-08-10T13:04:20-05:00', 'moddate': "D:20200819005507Z00'00'", 'gts_pdfxversion': 'PDF/X-1:2001'}, page_content='194  ·  THE ALMANACK OF NAVAL RAVIKANT\nTHE MEANINGS OF LIFE\nA really unbounded, big question: what is the meaning and \npurpose of life?\nThat’ s a big question. Because it’ s a big question, I’ll give you \nthree answers.\nAnswer 1: It’ s personal. You have to find your own meaning. \nAny piece of wisdom anybody else gives you, whether it’ s \nBuddha or me, is going to sound like nonsense. Fundamentally, \nyou have to find it for yourself, so the important part is not \nthe answer, it’ s the question. You just have to sit there and dig \nwith the question. It might take you years or decades. When \nyou find an answer you’re happy with, it will be fundamental \nto your life.\nAnswer 2: There is no meaning to life. There is no purpose to \nlife. Osho said, “It’ s like writing on 
# water or building houses \nof sand.” The reality is you’ve been dead for the history of the \nUniverse, 10 billion years or more. You 
# will be dead for the \nnext 70 billion years or so, until the heat death of the Universe.\nAnything you do will fade. It will disappear, just like the human \nrace will disappear and the planet will disappear. Even the \ngroup who colonizes Mars will disappear. No one is going to \nremember you past a certain number of generations, whether \nyou’re an artist, a poet, a conqueror, a pauper, or anyone else. \nThere’ s no meaning.\nYou have to create your own meaning, which is what it boils \ndown to. You have to decide:\n“Is this a 
# play I’m just watching?”'), Document(metadata={'title': 'Eric-Jorgenson_The-Almanack-of-Naval-Ravikant.indd', 'creationdate': '2020-08-10T13:04:20-05:00', 'source': '../../../Desktop/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf', 'trapped': '/False', 'creator': 'Adobe InDesign 15.1 (Macintosh)', 'producer': 'macOS Version 10.15.5 (Build 19F101) Quartz PDFContext, AppendMode 1.1', 'moddate': "D:20200819005507Z00'00'", 'gts_pdfxconformance': 'PDF/X-1a:2001', 'page_label': '195', 'gts_pdfxversion': 'PDF/X-1:2001', 'page': 
# # 194, 'total_pages': 242}, page_content='PHILOSOPHY ·  195\n“Is there a self-actualization dance I’m doing?”\n“Is there a specific thing I desire just for the heck of it?”\nThese are all meanings you make up.\nThere is no fundamental, intrinsic purposeful meaning to \nthe Universe. If there was, then you would just ask the next \nquestion. You’d say, “Why is that the meaning?” It would be, \nas physicist Richard Feynman said, it would be “turtles all the \nway down.” The “why’ s” would keep accumulating. There is no \nanswer you could give that wouldn’t have another “why.”\nI don’t buy the everlasting afterlife answers because it’ s insane \nto me, with absolutely no evidence, to believe because of how \nyou live seventy years here on this planet, you’re going to spend \neternity, which is a very long time, in some afterlife. What kind \nof silly God judges you for eternity based on some small period \nof time here? I think after this life, it’ s very much like before \nyou were born. Remember that? It’ s going to be just like that.\nBefore you were born, you didn’t care about anything or \nanyone, including your loved ones, including yourself, includ-\ning humans, including whether we go to Mars or whether we \nstay on planet Earth, whether there’ s an AI or not. After death, \nyou just don’t care either.\nAnswer 3: The last answer I’ll give you is a little more complicated. \nFrom what I’ve read in science (friends of mine have written \nbooks on this), I’ve stitched together some theories. Maybe there \nis a meaning to life, but it’ s not a very satisfying purpose.\nBasically, in physics, the arrow of time comes from entropy.')]   



                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    query_loop()
    
