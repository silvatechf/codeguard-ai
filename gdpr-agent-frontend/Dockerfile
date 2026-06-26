# Estágio 1: Build do Angular
FROM node:22-alpine as build

WORKDIR /app

# Aumenta o limite de memória do Node para evitar crashes no build (boa prática!)
ENV NODE_OPTIONS="--max-old-space-size=4096"

# Copia arquivos de dependência
COPY package*.json ./

# Instala dependências ignorando conflitos opcionais
RUN npm install --legacy-peer-deps

# Copia o código fonte
COPY . .

# Executa o build (CORREÇÃO AQUI: Adicionar --base-href /)
# Isso garante que o Angular gere caminhos de assets corretamente (ex: /main.js em vez de main.js)
RUN npx ng build --configuration=production --base-href /

# Estágio 2: Servidor Web (Nginx)
FROM nginx:alpine

# Copia o resultado do build
# O caminho aqui está correto, conforme confirmado pelo seu `docker exec`
COPY --from=build /app/dist/gdpr-agent-frontend/browser /usr/share/nginx/html

# Copia configuração do Nginx (Assumindo que você está usando o .conf revisado)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]