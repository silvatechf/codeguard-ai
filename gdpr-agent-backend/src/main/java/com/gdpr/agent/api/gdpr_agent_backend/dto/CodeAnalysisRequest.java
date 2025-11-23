package com.gdpr.agent.api.gdpr_agent_backend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

// DTO que representa a requisição vinda do Angular
public class CodeAnalysisRequest {

    // O código Java enviado pelo usuário
    @NotBlank(message = "The code must not be empty.")
    @Size(min = 10, message = "Code snippet is too short for analysis.")
    private String javaCode;

    // NOVO CAMPO: O idioma escolhido (en, pt, es, etc.)
    // Não colocamos @NotBlank porque se vier vazio, assumimos inglês no getter.
    private String language;

    // Construtor Padrão (Obrigatório para o Jackson/Spring)
    public CodeAnalysisRequest() {}

    public CodeAnalysisRequest(String javaCode, String language) {
        this.javaCode = javaCode;
        this.language = language;
    }

    // --- Getters e Setters ---

    public String getJavaCode() {
        return javaCode;
    }

    public void setJavaCode(String javaCode) {
        this.javaCode = javaCode;
    }

    public String getLanguage() {
        // Lógica de Segurança: Se o front não mandar nada, garantimos "en" (inglês)
        // Isso evita NullPointerException lá no Python
        return language != null ? language : "en";
    }

    public void setLanguage(String language) {
        this.language = language;
    }
}