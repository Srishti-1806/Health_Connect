import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from fpdf import FPDF
import tempfile

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq

app = FastAPI(title="Groq PDF Summarizer API", version="1.0")

# Load Groq API key from .env
def load_groq_api_key():
    dotenv_path = "groq.env"
    load_dotenv(dotenv_path)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError(f"Unable to retrieve GROQ_API_KEY from {dotenv_path}")
    return groq_api_key

# Text chunking + vector store
def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    knowledge_base = Chroma.from_texts(chunks, embeddings)
    return knowledge_base

# Generate summary PDF
def generate_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="PDF Summary", align="L")
    pdf.ln(5)

    for line in summary_text.split('\n'):
        if line.strip():
            pdf.multi_cell(0, 10, txt=f"• {line.strip()}", align="L")

    output_path = os.path.join(tempfile.gettempdir(), "summary_output.pdf")
    pdf.output(output_path)
    return output_path

@app.on_event("startup")
def startup_event():
    try:
        os.environ["GROQ_API_KEY"] = load_groq_api_key()
        print("✅ Groq API key loaded successfully.")
    except ValueError as e:
        print("❌", str(e))

@app.post("/api/summarize")
async def summarize_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        # Read PDF content
        pdf_reader = PdfReader(file.file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        if not text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in the PDF.")

        # Process and summarize
        knowledge_base = process_text(text)
        query = (
            "Summarize the content of the uploaded PDF file in approximately 3-5 sentences. "
            "Focus on capturing the main ideas and key points discussed in the document. "
            "Use your own words and ensure clarity and coherence in the summary."
        )

        docs = knowledge_base.similarity_search(query)

        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-70b-8192",
            temperature=0.1
        )

        chain = load_qa_chain(llm, chain_type='stuff')
        response = chain.run(input_documents=docs, question=query)

        # Generate PDF
        pdf_path = generate_pdf(response)

        return {
            "summary": response,
            "pdf_path": pdf_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download")
async def download_summary():
    pdf_path = os.path.join(tempfile.gettempdir(), "summary_output.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Summary PDF not found.")
    return FileResponse(pdf_path, filename="summary.pdf", media_type="application/pdf")

@app.get("/")
def root():
    return {"message": "📄 Groq PDF Summarizer API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
