import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html', // Agora aponta para o nome correto
  styleUrls: ['./app.component.scss'], // Se tiver css, mude para .css
  standalone: false
})
export class AppComponent {
  title = 'gdpr-agent-frontend';
}