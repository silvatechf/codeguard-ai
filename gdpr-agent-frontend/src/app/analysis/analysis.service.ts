import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CodeAnalysisRequest {
  javaCode: string; // Mantido por compatibilidade com o front, representa o código enviado
  language?: string;
}

export interface CodeAnalysisResponse {
  success: boolean;
  message: string;      // O relatório markdown robusto vindo direto da IA
  fixedCode?: string;    // O código corrigido e refatorado pela IA
  codeLength: number;
  securityScore: number; // Lido direto do backend (0-100)
  riskLevel: string;     // Lido direto do backend (LOW, MEDIUM, HIGH, CRITICAL)
  gdprStatus: string;    // Adicionado ao payload real do backend
  issuesCount: number;   // Adicionado ao payload real do backend
}

@Injectable({
  providedIn: 'root'
})
export class AnalysisService {
  // Agora aponta para a nossa rota unificada do Django Ninja
  private apiUrl = 'http://localhost:8000/api/v1/auditor/analyze';

  constructor(private http: HttpClient) { }

  analyzeCode(codeRequest: CodeAnalysisRequest): Observable<CodeAnalysisResponse> {
    return this.http.post<CodeAnalysisResponse>(this.apiUrl, codeRequest);
  }
}