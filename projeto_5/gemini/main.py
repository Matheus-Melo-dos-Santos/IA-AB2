import gradio as gr
from dotenv import load_dotenv
import os

from src.pdf_processor import PDFProcessor
from src.rag_system import RAGSystem

# Carrega as variáveis de ambiente (como chaves de API)
load_dotenv()

# Verifica se a chave de API do Gemini está configurada
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY não encontrada. Por favor, configure-a no arquivo .env.")

# Inicializa o sistema RAG (placeholder)
rag_system = None

def process_and_chat(pdf_file, user_question):
    global rag_system # Usar a variável global para o sistema RAG

    if pdf_file is None:
        return "Por favor, faça o upload de um arquivo PDF primeiro."

    # --- Fase de Processamento e Indexação ---
    if rag_system is None: # Se o sistema ainda não foi inicializado para este PDF
        try:
            yield "Status do Processamento: Carregando e dividindo PDF..."
            # 1. Carregar e Processar PDF
            documents = PDFProcessor.load_and_split_pdf(pdf_file.name)
            
            yield "Status do Processamento: Inicializando LLM e Embeddings (Gemini 1.5 Flash)..."
            # 2. Inicializar o LLM e Embeddings do Gemini
            from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
            from langchain.vectorstores import Chroma

            # Instanciando o modelo Gemini 1.5 Flash para chat
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1) # Temperatura mais baixa para respostas mais factuais
            
            # Instanciando o modelo de Embeddings do Gemini
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # Modelo de embedding do Gemini

            yield "Status do Processamento: Criando/carregando Vector Store..."
            # Cria e persiste o VectorStore (ou carrega se já existe)
            # Para este exemplo, criamos na memória a cada upload, o que é ineficiente para múltiplos chats.
            # Num app real, você persistiria o ChromaDB em disco.
            vectorstore = Chroma.from_documents(documents, embeddings)
            rag_system = RAGSystem(llm=llm, vectorstore=vectorstore)

            yield "Status do Processamento: PDF processado e indexado com sucesso! Agora você pode fazer perguntas."

        except Exception as e:
            yield f"Erro ao processar PDF: {e}"
            rag_system = None # Reseta o sistema em caso de erro

    if rag_system is None:
        return "Erro: Sistema RAG não inicializado após processamento do PDF."

    # --- Fase de Conversação ---
    if not user_question:
        return "Por favor, digite sua pergunta."

    try:
        response = rag_system.query_document(user_question)
        return response
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"


# --- Interface Gradio ---
with gr.Blocks() as demo:
    gr.Markdown("# Agente Conversacional para PDF com LLM (Gemini 1.5 Flash) e RAG")
    gr.Markdown("Faça o upload de um PDF, aguarde o processamento, e então converse sobre seu conteúdo.")

    with gr.Row():
        pdf_upload = gr.File(label="Upload PDF", file_types=[".pdf"])
        # Botão para processar o PDF (opcional, para feedback claro)
        process_btn = gr.Button("Processar PDF")
    
    status_output = gr.Textbox(label="Status do Processamento", interactive=False, value="Aguardando upload de PDF...")

    with gr.Column():
        chatbot = gr.Chatbot(label="Conversa")
        msg = gr.Textbox(label="Sua Pergunta")
        clear = gr.ClearButton([msg, chatbot, pdf_upload, status_output])

    def user_message(user_msg, chat_history):
        # Adiciona a mensagem do usuário ao histórico
        chat_history.append((user_msg, None))
        return "", chat_history

    # Handler para o processamento do PDF
    def handle_pdf_upload(file_obj):
        global rag_system
        rag_system = None # Reseta o sistema RAG para um novo PDF
        if file_obj:
            # O processo de upload e inicialização do RAG será feito em predict_candidate_selection
            # ou em um processo separado para feedback de status
            
            # Aqui, para o Gradio, o `process_and_chat` será chamado no `submit` do `msg`
            # ou você pode fazer uma função separada para lidar com o upload e o processamento inicial
            
            # Para este exemplo, o `process_btn` chamará esta função para iniciar o processamento
            # e atualizar o status_output.
            
            status_output_val = "Processando PDF..."
            # O processamento pesado (carregar, chunk, embedding, indexar)
            # pode ser chamado aqui e seu resultado (o rag_system inicializado)
            # armazenado globalmente ou passado para a próxima fase.
            try:
                documents = PDFProcessor.load_and_split_pdf(file_obj.name)
                
                from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
                from langchain.vectorstores import Chroma

                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

                vectorstore = Chroma.from_documents(documents, embeddings)
                rag_system = RAGSystem(llm=llm, vectorstore=vectorstore)
                status_output_val = "PDF processado e indexado com sucesso! Agora você pode fazer perguntas."
            except Exception as e:
                status_output_val = f"Erro ao processar PDF: {e}"
                rag_system = None # Reseta o sistema em caso de erro

            return status_output_val
        else:
            return "Nenhum PDF selecionado."

    process_btn.click(handle_pdf_upload, inputs=[pdf_upload], outputs=[status_output])

    def respond(user_msg, chat_history):
        # Adiciona a mensagem do usuário ao histórico antes de gerar a resposta
        chat_history.append((user_msg, None)) # User message, response placeholder
        
        if rag_system is None:
            chat_history[-1] = (user_msg, "Por favor, faça o upload e processe um arquivo PDF antes de perguntar.")
            return chat_history, gr.update(value="") # Clear msg input
        
        try:
            response = rag_system.query_document(user_msg)
            chat_history[-1] = (user_msg, response) # Update response
        except Exception as e:
            chat_history[-1] = (user_msg, f"Erro ao gerar resposta: {e}")
        
        return chat_history, gr.update(value="") # Clear msg input

    msg.submit(user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
        respond, inputs=[msg, chatbot], outputs=[chatbot, msg]
    )

demo.launch()