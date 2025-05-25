# src/pdf_processor.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFProcessor:
    @staticmethod
    def load_and_split_pdf(pdf_path: str):
        """
        Carrega um PDF e divide seu texto em chunks.
        """
        print(f"Loading PDF from {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"PDF split into {len(chunks)} chunks.")
        return chunks