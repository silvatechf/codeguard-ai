import os
import json
import re
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
# Importando as exceções de API mais comuns
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)
CORS(app)

# Validação da API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # MUDANÇA: Não use a API Key se ela não for encontrada, evite erros de configuração
    logger.error("❌ ERROR: API Key not found in .env file! AI functions will fail.")
else:
    genai.configure(api_key=api_key)
    logger.info("✅ API Key loaded.")

def extract_json(text):
# ... (Função extract_json é mantida igual)
    """Extrai JSON de forma robusta, ignorando formatações extras da IA"""
    try:
        # Tenta limpar blocos de markdown comuns
        clean = text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except:
        try:
            # Procura pelo primeiro '{' e o último '}'
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match: return json.loads(match.group())
        except: pass
    return None


@app.route('/analyze/code', methods=['POST'])
def analyze_code():
    # Primeira verificação: se a chave da API falhou ao carregar
    if not api_key:
        return jsonify({"status": "error", "summary": "API Key não configurada no servidor."}), 500

    try:
        data = request.json
        java_code = data.get('javaCode', '')
        language = data.get('language', 'en')
        
        # Mapeamento de idiomas
        lang_map = {
            'pt': 'Portuguese (Brasil)',
            'es': 'Spanish',
            'fr': 'French',
            'it': 'Italian',
            'de': 'German',
            'en': 'English'
        }
        selected_lang = lang_map.get(language, 'English')

        logger.info(f"Analyzing code request. Lang: {selected_lang}")

        # Prompt Otimizado para JSON
        prompt = f"""
        Act as a Senior Security Auditor. Analyze this code:
        {java_code}
        
        OUTPUT JSON ONLY with these exact keys:
        - "markdown_report": Report in {selected_lang}.
        - "fixed_code": Secure code.
        - "security_score": Integer 0-100.
        - "risk_level": String ("LOW", "MEDIUM", "HIGH", "CRITICAL").
        """

        # CORREÇÃO CRÍTICA: Trocando o nome do modelo para um suportado e atual
        # gemini-2.5-flash é a versão estável mais recente do modelo Flash
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        ai_output = extract_json(response.text)
        
        if not ai_output:
            return jsonify({
                 "status": "success",
                 "summary": response.text,
                 "fixed_code": "// Error parsing AI JSON. Check report.",
                 "security_score": 50,
                 "risk_level": "MEDIUM"
               })

        return jsonify({
            "status": "success",
            "summary": ai_output.get("markdown_report") or ai_output.get("summary"),
            "fixed_code": ai_output.get("fixed_code"),
            "security_score": ai_output.get("security_score", 0),
            "risk_level": ai_output.get("risk_level", "UNKNOWN")
        })

    # TRATAMENTO ESPECÍFICO PARA ERROS DA API GEMINI
    except ResourceExhausted:
        error_msg = "Limite de Quota da API excedido. Tente novamente mais tarde."
        logger.error(f"API Error: {error_msg}")
        return jsonify({"status": "error", "summary": error_msg}), 500

    except GoogleAPICallError as e:
        error_msg = f"Erro na chamada da API Google: {str(e)}"
        logger.error(f"API Error: {error_msg}")
        return jsonify({"status": "error", "summary": error_msg}), 500

    except Exception as e:
        logger.error(f"General AI Engine Error: {e}", exc_info=True) # Adicionado exc_info=True para logar o traceback
        return jsonify({"status": "error", "summary": f"Erro interno do servidor: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting AI Engine on port 5000...")
    # Configuração para Docker: host 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)