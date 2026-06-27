import { Component } from '@angular/core';
import { AnalysisService, CodeAnalysisResponse } from '../analysis/analysis.service';

@Component({
  selector: 'app-agent-dashboard',
  templateUrl: './agent-dashboard.component.html',
  styleUrls: ['./agent-dashboard.component.scss'],
  standalone: false
})
export class AgentDashboardComponent {
  javaCode: string = '';
  selectedLanguage: string = 'en'; 
  analysisResult: CodeAnalysisResponse | null = null;
  isLoading: boolean = false;
  isMobileMenuOpen: boolean = false;
  activeTab: 'report' | 'fixed' = 'report';
  currentDemoLabel: string = '';
  private exampleIndex: number = 0;

  // Métricas extraídas diretamente do payload real
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
        code: `@RestController\n@RequestMapping("/api/payments")\npublic class PaymentController {\n    private String awsAccessKey = "AKIA1234567890EXAMPLE";\n\n    @GetMapping("/pay/{userId}")\n    public String process(@PathVariable String userId) {\n        System.out.println("Processing sensitive user: " + userId);\n        return "Payment Processed";\n    }\n}`
      },
      {
        label: "Node.js (Express) - SQL Injection",
        code: `const express = require('express');\nconst app = express();\n\napp.post('/login', (req, res) => {\n  const { email, password } = req.body;\n  const query = "SELECT * FROM users WHERE email = '" + email + "'";\n  db.execute(query);\n});`
      },
      {
        label: "Python (Data Science) - S3 Data Leak",
        code: `import pandas as pd\nimport boto3\n\ndef export_eu_customers():\n    df = pd.read_csv("eu_customers_database.csv")\n    df.to_csv("s3://public-bucket-us-east-1/backup.csv")`
      }
    ];

    const currentExample = examples[this.exampleIndex];
    this.javaCode = currentExample.code;
    this.currentDemoLabel = currentExample.label; 
    this.isMobileMenuOpen = false;
    this.exampleIndex = (this.exampleIndex + 1) % examples.length;
  }

  analyzeCode(): void {
    if (!this.javaCode) return;

    this.isLoading = true;
    this.analysisResult = null; 
    this.activeTab = 'report';
    
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
          // PROIBIDO CALCULAR NO FRONT: Mapeamento direto de propriedades reais do contrato
          this.securityScore = response.securityScore; 
          this.riskLevel = response.riskLevel;
          this.gdprStatus = response.gdprStatus;
          this.issuesCount = response.issuesCount;
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.analysisResult = { 
          success: false, 
          message: '### System Error\nConnection to unified Django backend failed.', 
          fixedCode: '', codeLength: 0, securityScore: 0, riskLevel: 'ERROR', gdprStatus: 'ERROR', issuesCount: 0
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