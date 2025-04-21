import os
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("groq_api_key")

# Setup embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Setup vectorstore
if os.path.exists("chat_memory/index.faiss"):
    vectorstore = FAISS.load_local(
        "chat_memory", embedding_model, allow_dangerous_deserialization=True
    )
else:
    dummy_doc = Document(page_content="This is a dummy initial document to create the index.")
    vectorstore = FAISS.from_documents([dummy_doc], embedding_model)
    vectorstore.save_local("chat_memory")

# Setup retriever and LLM
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
llm = ChatGroq(api_key=groq_api_key, model_name="llama3-8b-8192")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Save new input into memory
def save_to_memory(user_input: str):
    doc = Document(page_content=user_input)
    vectorstore.add_documents([doc])
    vectorstore.save_local("chat_memory")

# Query with memory context
def check_contextual_and_respond(user_input: str) -> str:
    save_to_memory(user_input)
    response = qa_chain.invoke(user_input)
    return response
