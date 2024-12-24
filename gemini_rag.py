import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_pinecone import PineconeVectorStore
from src.helper import download_hugging_face_embeddings


load_dotenv()

# Initialize environment variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
# PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Ensure API keys are set
if not PINECONE_API_KEY:
    raise ValueError("Pinecone API credentials are not set.")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key is not set.")

# Initialize HuggingFace embeddings
def initialize_embeddings():
    """Download or initialize embeddings."""
    return download_hugging_face_embeddings()

embeddings = initialize_embeddings()

# Define Pinecone index name (ensure it matches your setup)
index_name = "interview-bot"

# Initialize Pinecone vector store
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize Google Gemini API
def initialize_gemini():
    """Initialize the Google Gemini API."""
    genai.configure(api_key=GOOGLE_API_KEY)
    return genai

gemini = initialize_gemini()

# RAG Retrieval and Generation
def retrieve_documents(query):
    """
    Retrieve relevant documents using the retriever.
    Args:
        query (str): User input query.
    Returns:
        str: Concatenated text of relevant documents.
    """
    docs = retriever.get_relevant_documents(query)
    return "\n".join([doc.page_content for doc in docs])


def generate_rag_response(query, model):
    """
    Generate a response using RAG (Retriever-Augmented Generation) approach.
    Args:
        query (str): User input query.
    Returns:
        str: Generated response.
    """
    # Retrieve relevant documents
    retrieved_docs = retrieve_documents(query)

    # Combine retrieved context with user query
    augmented_prompt = f"Context:\n{retrieved_docs}\n\nQuery: {query}\nNOTE: Act as a interview expert and use the given context.\nAnswer:"

    # Generate response using Gemini
    try:
        response = model.generate_content(augmented_prompt)
        return response.text
    except Exception as e:
        return f"Error in generating response: {e}"

# load the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Chat application loop
def main():
    print("Welcome to the RAG Chat! Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Generate RAG response
        response = generate_rag_response(user_input, model)
        print("RAG: ", response)

if __name__ == "__main__":
    main()
