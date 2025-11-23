import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Carrega a chave
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print(f"🔑 Testando chave: {str(api_key)[:5]}...******")

if not api_key:
    print("❌ ERRO: Chave não encontrada no arquivo .env")
    exit()

# 2. Configura
try:
    genai.configure(api_key=api_key)
    print("✅ Configuração inicial OK.")
except Exception as e:
    print(f"❌ Erro de configuração: {e}")
    exit()

# 3. Pergunta ao Google quais modelos você pode usar
print("\n📡 Consultando modelos disponíveis para sua chave...")
try:
    found_model = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   - Modelo disponível: {m.name}")
            found_model = True
    
    if not found_model:
        print("⚠️ A conexão funcionou, mas nenhum modelo de texto foi encontrado. Verifique as permissões da chave.")
    else:
        print("\n✅ SUCESSO! Sua chave está funcionando e tem acesso à API.")

except Exception as e:
    print(f"❌ ERRO CRÍTICO DE CONEXÃO: {e}")
    print("Dica: Verifique se sua internet bloqueia APIs ou se a chave foi cancelada.")