import { Component } from '@angular/core';
import { AnalysisService, CodeAnalysisResponse } from '../analysis/analysis.service';

@Component({
  selector: 'app-agent-dashboard',
  templateUrl: './agent-dashboard.component.html',
  styleUrls: ['./agent-dashboard.component.scss'],
  standalone: false
})
export class AgentDashboardComponent {
  
  // Estados
  javaCode: string = '';
  selectedLanguage: string = 'en'; 
  analysisResult: CodeAnalysisResponse | null = null;
  isLoading: boolean = false;
  isMobileMenuOpen: boolean = false;
  activeTab: 'report' | 'fixed' = 'report';
  currentDemoLabel: string = '';
  private exampleIndex: number = 0;

  // Métricas (Iniciam zeradas) - ADICIONADAS AQUI PARA CORRIGIR O ERRO
  securityScore: number = 0;
  riskLevel: string = '-';
  gdprStatus: string = '-';
  issuesCount: number = 0;

  constructor(private analysisService: AnalysisService) {}

  setActiveTab(tab: 'report' | 'fixed'): void { this.activeTab = tab; }
  toggleMobileMenu(): void { this.isMobileMenuOpen = !this.isMobileMenuOpen; }

  fillExampleCode(): void {
    const examples = [
      {
        label: "Java (Spring Boot) - Cloud & Log Risk",
        code: `@RestController
@RequestMapping("/api/payments")
public class PaymentController {
    // 🚨 CLOUD RISK: Hardcoded AWS Credentials
    // This violates cloud security best practices
    private String awsAccessKey = "AKIA1234567890EXAMPLE"; 

    @GetMapping("/pay/{userId}")
    public String process(@PathVariable String userId) {
        // 🚨 GDPR RISK: Logging PII (User ID) directly
        System.out.println("Processing sensitive user: " + userId); 
        return "Payment Processed";
    }
}`
      },
      {
        label: "Node.js (Express) - SQL Injection",
        code: `const express = require('express');
const app = express();

app.post('/login', (req, res) => {
  const { email, password } = req.body;
  
  // 🚨 SECURITY RISK: SQL Injection Vulnerability
  // Direct concatenation of user input into query
  const query = "SELECT * FROM users WHERE email = '" + email + "'";
  
  console.log("Executing: " + query); // PII Leak in logs
  db.execute(query);
});`
      },
      {
        label: "Python (Data Science) - S3 Data Leak",
        code: `import pandas as pd
import boto3

def export_eu_customers():
    # Loading sensitive customer data
    df = pd.read_csv("eu_customers_database.csv")
    
    # 🚨 GDPR & SOVEREIGNTY RISK: 
    # Sending EU Citizen data to a Public Bucket in the US
    # This violates data residency laws
    df.to_csv("s3://public-bucket-us-east-1/backup.csv")
    
    print("Backup completed to Public Cloud")`
      }
    ];

    // 1. Pega o exemplo baseado no índice atual
    const currentExample = examples[this.exampleIndex];
    
    // 2. Atualiza a tela
    this.javaCode = currentExample.code;
    this.currentDemoLabel = currentExample.label; 
    
    // Fecha o menu mobile se estiver aberto (Melhoria de UX)
    this.isMobileMenuOpen = false;

    // 3. Prepara o índice para o próximo clique (0 -> 1 -> 2 -> 0...)
    this.exampleIndex = (this.exampleIndex + 1) % examples.length;
  }

  analyzeCode(): void {
    if (!this.javaCode) return;

    this.isLoading = true;
    this.analysisResult = null; 
    this.activeTab = 'report';
    
    // Reset Metrics while loading
    this.securityScore = 0;
    this.issuesCount = 0;
    this.riskLevel = '-';
    this.gdprStatus = '-';
    
    this.analysisService.analyzeCode({ 
      javaCode: this.javaCode,
      language: this.selectedLanguage 
    }).subscribe({
      next: (response) => {
        this.analysisResult = response;
        this.isLoading = false;
        
        if (response.success) {
            // AQUI ESTÁ A CORREÇÃO FINAL:
            // Lemos direto do backend. Não calculamos nada.
            this.securityScore = response.securityScore; 
            this.riskLevel = response.riskLevel;
            
            // Lógica visual simples
            this.gdprStatus = this.securityScore < 80 ? 'NON-COMPLIANT' : 'COMPLIANT';
            this.issuesCount = Math.max(1, Math.round((100 - this.securityScore) / 15));
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.analysisResult = { 
            success: false, 
            message: '### System Error\nConnection failed.', 
            fixedCode: '', codeLength: 0, securityScore: 0, riskLevel: 'ERROR' 
        };
      }
    });
  }

  copyReport(): void {
    const textToCopy = this.activeTab === 'report' 
      ? this.analysisResult?.message 
      : this.analysisResult?.fixedCode;

    if (textToCopy) {
      navigator.clipboard.writeText(textToCopy).then(() => {
        alert('Content copied to clipboard!'); 
      });
    }
  }
  
  changeLanguage(event: Event): void {
    const target = event.target as HTMLSelectElement;
    this.selectedLanguage = target.value;
  }
}