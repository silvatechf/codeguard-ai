package com.gdpr.agent.api.gdpr_agent_backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class PythonAgentResponse {
    
    private String status;
    
    // Mapeia o campo "markdown_report" do JSON do Python para "summary"
    @JsonProperty("markdown_report") 
    private String summary;
    
    // Alternativa caso o Python mande como "summary" (retrocompatibilidade)
    @JsonProperty("summary")
    private void unpackSummary(String summary) {
        if (this.summary == null) this.summary = summary;
    }

    @JsonProperty("fixed_code") 
    private String fixedCode; 

    @JsonProperty("security_score")
    private int securityScore;

    @JsonProperty("risk_level")
    private String riskLevel;

    // Getters e Setters
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public String getSummary() { return summary; }
    public void setSummary(String summary) { this.summary = summary; }
    
    public String getFixedCode() { return fixedCode; } 
    public void setFixedCode(String fixedCode) { this.fixedCode = fixedCode; }

    public int getSecurityScore() { return securityScore; }
    public void setSecurityScore(int securityScore) { this.securityScore = securityScore; }

    public String getRiskLevel() { return riskLevel; }
    public void setRiskLevel(String riskLevel) { this.riskLevel = riskLevel; }
}