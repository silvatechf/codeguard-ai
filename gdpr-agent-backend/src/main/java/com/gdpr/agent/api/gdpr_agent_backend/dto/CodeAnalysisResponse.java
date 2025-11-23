package com.gdpr.agent.api.gdpr_agent_backend.dto;

public class CodeAnalysisResponse {

    private boolean success;
    private String message;
    private String fixedCode;
    private int codeLength;
    private int securityScore;
    private String riskLevel;

    // Construtor Completo (6 argumentos)
    public CodeAnalysisResponse(boolean success, String message, String fixedCode, int codeLength, int securityScore, String riskLevel) {
        this.success = success;
        this.message = message;
        this.fixedCode = fixedCode;
        this.codeLength = codeLength;
        this.securityScore = securityScore;
        this.riskLevel = riskLevel;
    }

    // Getters e Setters
    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }
    public String getFixedCode() { return fixedCode; }
    public int getCodeLength() { return codeLength; }
    public int getSecurityScore() { return securityScore; }
    public String getRiskLevel() { return riskLevel; }
}