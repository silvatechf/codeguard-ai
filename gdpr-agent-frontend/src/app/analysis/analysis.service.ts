import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CodeAnalysisRequest {
  javaCode: string;
  language?: string;
}

export interface CodeAnalysisResponse {
  success: boolean;
  message: string;
  fixedCode?: string;
  codeLength: number;
  securityScore: number;
  riskLevel: string;
}

@Injectable({
  providedIn: 'root'
})
export class AnalysisService {

  // URL RELATIVA: O Nginx vai interceptar isso.
  // Não coloque 'http://localhost:8080' aqui!
  private apiUrl = '/api/v1/analysis/submit';

  constructor(private http: HttpClient) { }

  analyzeCode(codeRequest: CodeAnalysisRequest): Observable<CodeAnalysisResponse> {
    console.log("Sending analysis request to Proxy:", this.apiUrl);
    return this.http.post<CodeAnalysisResponse>(this.apiUrl, codeRequest);
  }
}