import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from pinecone import ServerlessSpec

from langchain_pinecone.vectorstores import PineconeVectorStore
from src.helper import load_files, text_split, download_hugging_face_embeddings

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

extracted_data = load_files("scraped_data")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


#Initializing the Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name="interview-bot"


# Check if the index already exists
try:
    pc.describe_index(index_name)
    print(f"Index '{index_name}' already exists.")
except Exception as e:
    if "not found" in str(e):
        print(f"Creating index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    else:
        raise  # Re-raise unexpected errors

# Now create the PineconeVectorStore
docsearch = PineconeVectorStore.from_texts([t.page_content for t in text_chunks], embeddings, index_name=index_name)
print("storing done!!!!")