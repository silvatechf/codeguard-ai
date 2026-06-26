// src/app/app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { MarkdownModule } from 'ngx-markdown'; // <--- IMPORTANTE

import { AppComponent } from './app.component';
import { AgentDashboardComponent } from './agent-dashboard/agent-dashboard.component';

@NgModule({
  declarations: [
    AppComponent,
    AgentDashboardComponent // <--- Seu componente declarado aqui
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    MarkdownModule.forRoot() // <--- O Markdown habilitado aqui
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }