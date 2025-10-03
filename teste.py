from ragflow_sdk import RAGFlow

# --------------------------
# CONFIGURAÇÃO
# --------------------------
API_KEY = "ragflow-Y2ODA1MzNhOWZjYzExZjBiZjliMzI2ND"
BASE_URL = "http://localhost:9380"
CHAT_ID = "90a38e4a9fca11f0a8edf29f1ba0db2d"  # consultAI

# Inicializa RAGFlow
rag = RAGFlow(api_key=API_KEY, base_url=BASE_URL)

# Lista chats disponíveis para verificar
chats = rag.list_chats()
print("Chats disponíveis com essa chave:")
for c in chats:
    print(c.id, c.name)

# Busca o chat pelo ID correto
assistant = next((c for c in chats if c.id == CHAT_ID), None)
if assistant is None:
    raise ValueError(f"Chat com ID {CHAT_ID} não encontrado.")

# Cria sessão de chat
session = assistant.create_session()

# --------------------------
# Função segura de ask
# --------------------------
def safe_ask(session, question):
    response_content = ""
    try:
        for ans in session.ask(question, stream=True):
            print(ans.content[len(response_content):], end='', flush=True)
            response_content = ans.content
    except KeyError:
        # Mensagem amigável caso haja problema com chunks
        if response_content.strip() == "":
            print("⚠️ Nenhuma informação relevante encontrada no dataset.")
        else:
            print("\n")
    print("\n------------------------------------------------------\n")

# --------------------------
# LOOP DE CONVERSA
# --------------------------
print("\n==================== Chat consultAI ====================\n")
while True:
    question = input("\nVocê: ")
    if question.lower() in ["sair", "exit", "quit"]:
        print("Encerrando chat...")
        break
    safe_ask(session, question)
