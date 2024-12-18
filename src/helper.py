from langchain.document_loaders import TextLoader, DirectoryLoader, UnstructuredFileLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


# Extract Data from Text, DOCX, and PDF Files
def load_files(data, file_type="pdf"):
    if file_type == "pdf":
        loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    elif file_type == "txt":
        loader = DirectoryLoader(data, glob="*.txt", loader_cls=TextLoader)
    elif file_type == "docx":
        loader = DirectoryLoader(data, glob="*.docx", loader_cls=UnstructuredFileLoader)
    else:
        raise ValueError("Unsupported file type. Use 'pdf', 'txt', or 'docx'.")

    documents = loader.load()
    return documents


# Split the Data into Text Chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


# Download the Embeddings from HuggingFace
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')  # this model returns 384 dimensions
    return embeddings