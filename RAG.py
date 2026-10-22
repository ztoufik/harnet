from typing import List
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
import os

from llm_provider import or_model
from load_pdf import load_pdf_pages

# 1. Load Environment Variables
load_dotenv("api_keys.txt")

# 2. Define Custom OpenRouter Embedding Class
class OpenRouterNvidiaEmbeddings(Embeddings):
    def __init__(self, model_name: str):
        self.model_name = model_name
        # Initialize standard OpenAI client pointed at OpenRouter
        self.client = OpenAI(
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url=os.environ["OPENROUTER_BASE_URL"],
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Send batch request to OpenRouter
        response = self.client.embeddings.create(
            input=texts,
            model=self.model_name
        )
        # Extract embeddings in the correct order
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> List[float]:
        # Send single string query request
        response = self.client.embeddings.create(
            input=[text],
            model=self.model_name
        )
        return response.data[0].embedding


# 3. Process Documents
file_path = "test_pdf.pdf"
docs = load_pdf_pages(file_path)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=50, add_start_index=True
)
documents = text_splitter.split_documents(docs)


# 4. Initialize Custom Embeddings & Vector Store
embeddings = OpenRouterNvidiaEmbeddings(
    model_name="nvidia/nemotron-3.5-embed-1b:free"
)

vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()


# 5. Set up RAG Chain
prompt = ChatPromptTemplate.from_template(
    """
    You are an expert assistant. Answer the following question based only on the provided context:
    
    <context>
    {context}
    </context>
    
    Question: {question}
    """
)

llm = or_model

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

retrieval_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)  


# 6. Invoke Chain
result = retrieval_chain.invoke("list all the libraries.")
print(result)
