# 1. Escolhe o Python como base (imagem leve e otimizada)
FROM python:3.10-slim

# 2. Cria uma pasta de trabalho lá dentro
WORKDIR /app

# 3. Instala ferramentas do sistema (build-essential é necessário se alguma biblioteca Python tiver dependências C)
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# 4. Copia o arquivo de requisitos do seu PC para o Container
COPY requirements.txt .

# 5. Instala as bibliotecas de forma única
# Sugestão: Adicione 'google-generativeai', 'python-dotenv', 'flask', e 'flask-cors'
# ao seu requirements.txt. Assim, esta única linha instala tudo de forma otimizada.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia TODO o seu código Python para dentro
# Esta etapa é executada por último para aproveitar o cache das camadas anteriores
COPY . .

# 7. Abre a porta (apenas documentação, não abre de fato a porta no host)
EXPOSE 5000

# 8. Roda o seu script
# Usar 0.0.0.0 garante que o Flask escute todas as interfaces de rede do contêiner
CMD ["python", "agent_api.py", "--host=0.0.0.0"]