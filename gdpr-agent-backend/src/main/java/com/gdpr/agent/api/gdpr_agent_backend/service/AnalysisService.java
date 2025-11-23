package com.gdpr.agent.api.gdpr_agent_backend.service;

import com.gdpr.agent.api.gdpr_agent_backend.dto.CodeAnalysisRequest;
import com.gdpr.agent.api.gdpr_agent_backend.dto.CodeAnalysisResponse;
import com.gdpr.agent.api.gdpr_agent_backend.dto.PythonAgentResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.math.BigInteger;

@Service
public class AnalysisService {

    private final WebClient webClient;
    
    // --- CORREÇÃO DO ERRO ---
    // Lógica Inteligente:
    // 1. Se houver uma variável de ambiente PYTHON_URL (Docker), usa ela.
    // 2. Se não (Teste Local no Windows), usa "http://localhost:5000".
    private String PYTHON_AGENT_URL = System.getenv("PYTHON_URL") != null 
                                      ? System.getenv("PYTHON_URL") 
                                      : "http://localhost:5000"; 

    // Cache em Memória
    private final Map<String, CodeAnalysisResponse> analysisCache = new ConcurrentHashMap<>();

    public AnalysisService(WebClient.Builder webClientBuilder) {
        System.out.println("🚀 AnalysisService Iniciado. Conectando na IA em: " + PYTHON_AGENT_URL);
        this.webClient = webClientBuilder.baseUrl(PYTHON_AGENT_URL).build();
    }

    public CodeAnalysisResponse analyzeCode(CodeAnalysisRequest request) {
        String codeHash = generateHash(request.getJavaCode() + request.getLanguage());

        // 1. Verifica Cache
        if (analysisCache.containsKey(codeHash)) {
            System.out.println("⚡ CACHE HIT: Retornando análise salva.");
            return analysisCache.get(codeHash);
        }

        // 2. Chama Python
        System.out.println("🐢 CACHE MISS: Chamando " + PYTHON_AGENT_URL + "...");

        try {
            PythonAgentResponse pythonResponse = webClient.post()
                    .uri("/analyze/code")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(PythonAgentResponse.class)
                    .timeout(Duration.ofSeconds(120)) 
                    .block();

            if (pythonResponse != null) {
                CodeAnalysisResponse response = new CodeAnalysisResponse(
                        "success".equals(pythonResponse.getStatus()),
                        pythonResponse.getSummary(),
                        pythonResponse.getFixedCode(),
                        request.getJavaCode().length(),
                        pythonResponse.getSecurityScore(),
                        pythonResponse.getRiskLevel() != null ? pythonResponse.getRiskLevel() : "UNKNOWN"
                );

                if (response.isSuccess()) {
                    analysisCache.put(codeHash, response);
                }
                
                return response;
            } else {
                return new CodeAnalysisResponse(false, "Empty response from AI.", null, 0, 0, "UNKNOWN");
            }

        } catch (Exception e) {
            // Loga o erro real no terminal para você ver
            System.err.println("❌ Erro de Conexão Java->Python: " + e.getMessage());
            return new CodeAnalysisResponse(false, "System Error: " + e.getMessage(), null, 0, 0, "UNKNOWN");
        }
    }

    private String generateHash(String input) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] messageDigest = md.digest(input.getBytes(StandardCharsets.UTF_8));
            return new BigInteger(1, messageDigest).toString(16);
        } catch (Exception e) {
            return String.valueOf(input.hashCode());
        }
    }
}