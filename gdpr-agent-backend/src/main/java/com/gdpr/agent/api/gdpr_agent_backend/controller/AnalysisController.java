package com.gdpr.agent.api.gdpr_agent_backend.controller;

import com.gdpr.agent.api.gdpr_agent_backend.dto.CodeAnalysisRequest;
import com.gdpr.agent.api.gdpr_agent_backend.dto.CodeAnalysisResponse;
import com.gdpr.agent.api.gdpr_agent_backend.service.AnalysisService; // <--- 1. IMPORTANTE: Importar o Serviço
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/analysis")
public class AnalysisController {

    // 2. DECLARAR A VARIÁVEL DO SERVIÇO
    // 'private final' garante que ela não mude depois de criada.
    private final AnalysisService analysisService;

    // 3. INJEÇÃO VIA CONSTRUTOR (A "Mágica" acontece aqui)
    // Quando o Spring cria o Controller, ele vê que precisa do AnalysisService
    // e o coloca aqui automaticamente.
    public AnalysisController(AnalysisService analysisService) {
        this.analysisService = analysisService;
    }

    @PostMapping("/submit")
    public ResponseEntity<CodeAnalysisResponse> analyzeCode(
            @Valid @RequestBody CodeAnalysisRequest request) {

        System.out.println("Received request from Angular. Calling Python Agent...");
        
        // 4. USAR O SERVIÇO
        // Agora podemos chamar o método que criamos no serviço
        CodeAnalysisResponse response = analysisService.analyzeCode(request);
        
        return ResponseEntity.ok(response);
    }
}