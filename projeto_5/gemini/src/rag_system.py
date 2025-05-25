# src/rag_system.py
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class RAGSystem:
    def __init__(self, llm, vectorstore):
        """
        Inicializa o sistema RAG.
        :param llm: Instância do Large Language Model (agora ChatGoogleGenerativeAI)
        :param vectorstore: Instância do VectorStore (Chroma) com os documentos indexados
        """
        self.llm = llm
        self.vectorstore = vectorstore
        
        self.custom_prompt_template = """Use the following context to answer the question at the end. 
        If the answer cannot be found in the context, politely state that you don't have enough information from the provided document.

        {context}

        Question: {question}
        Helpful Answer:"""
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff", # "stuff" coloca todos os documentos no prompt
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True, # Para justificativas
            chain_type_kwargs={"prompt": PromptTemplate(template=self.custom_prompt_template, input_variables=["context", "question"])}
        )

    def query_document(self, query: str) -> str:
        """
        Executa uma consulta contra os documentos indexados.
        """
        print(f"Querying: {query}")
        result = self.qa_chain.invoke({"query": query})

        # Para exibir a justificativa (trechos do documento) junto com a resposta
        response_text = result['result']
        source_docs = "\n".join([f"- ...{doc.page_content[:200]}..." for doc in result['source_documents']]) # Limita o trecho
        
        return f"{response_text}\n\n**Conteúdo de Referência no Documento:**\n{source_docs}"