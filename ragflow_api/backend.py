from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ragflow_sdk import RAGFlow

# --------------------------
# CONFIGURAÇÃO DO RAGFlow
# --------------------------
API_KEY = "ragflow-Y2ODA1MzNhOWZjYzExZjBiZjliMzI2ND"
BASE_URL = "http://localhost:9380"
CHAT_ID = "90a38e4a9fca11f0a8edf29f1ba0db2d"

rag = RAGFlow(api_key=API_KEY, base_url=BASE_URL)
chats = rag.list_chats()
assistant = next((c for c in chats if c.id == CHAT_ID), None)
if assistant is None:
    raise ValueError(f"Chat com ID {CHAT_ID} não encontrado.")
session = assistant.create_session()

# --------------------------
# FastAPI
# --------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Question(BaseModel):
    text: str

# --------------------------
# Função para limpar resposta
# --------------------------
def clean_response(ans_content: str) -> str:
    """
    Limpa o conteúdo retornado pelo modelo:
    - Remove mensagens de chunks
    - Remove informações técnicas como 'Categoria' ou 'Sinônimos'
    """
    # Remove tudo depois de frases tipo "Aqui estão as informações relevantes"
    if "Aqui estão as informações relevantes" in ans_content:
        ans_content = ans_content.split("Aqui estão as informações relevantes")[0]
    
    # Remove outras possíveis marcações repetidas
    for marker in ["⚠️ Atenção:", "Categoria:", "Sinônimos:"]:
        if marker in ans_content:
            ans_content = ans_content.split(marker)[0]
    
    return ans_content.strip()

# --------------------------
# Função segura de ask
# --------------------------
def safe_ask(session, question_text: str) -> str:
    """Evita duplicação de chunks e KeyError, e limpa a resposta"""
    response_content = ""
    previous_content = ""
    try:
        for ans in session.ask(question_text, stream=True):
            new_chunk = ans.content[len(previous_content):]
            if new_chunk.strip():
                response_content += new_chunk
            previous_content = ans.content
    except KeyError:
        if response_content.strip() == "":
            response_content = "⚠️ Nenhuma informação relevante encontrada no dataset."
    
    # Limpa a resposta antes de retornar
    return clean_response(response_content)

@app.post("/ask")
async def ask_question(q: Question):
    answer = safe_ask(session, q.text)
    return {"answer": answer}
