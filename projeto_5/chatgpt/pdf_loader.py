import fitz  # PyMuPDF

def carregar_texto_pdf(uploaded_file):
    texto = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto