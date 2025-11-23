# Etapa 1: Construção (Usa Maven para criar o JAR)
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app
# Copia o pom.xml e a pasta src do seu PC
COPY pom.xml .
COPY src ./src
# Roda o comando de build (pula testes para ser rápido)
RUN mvn clean package -DskipTests

# Etapa 2: Execução (Pega só o JAR pronto, super leve)
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
# Pega o arquivo .jar gerado na etapa anterior
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]