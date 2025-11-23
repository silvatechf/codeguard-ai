🛡️ CodeGuard AI - Intelligent Security Auditor

"Automating Compliance & Security for Modern DevSecOps Pipelines"

CodeGuard AI is an enterprise-grade security tool designed to detect GDPR violations, Cloud Security risks, and PII leaks directly in the source code. Powered by Google's Gemini 2.0 Flash LLM, it acts as a Senior Security Auditor, providing context-aware analysis and auto-remediation code fixes.

🚀 Key Features

🧠 Context-Aware AI Analysis

Unlike traditional regex-based scanners (SAST), CodeGuard understands the intent of the code.

False Positive Reduction: Distinguishes between a variable named password and an actual hardcoded credential.

Multi-Language Support: Analyzes Java, Python, Node.js, Terraform, and more.

🇪🇺 GDPR & Privacy Specialist

Specifically trained to detect violations of EU General Data Protection Regulation:

Data Minimization: Detects unnecessary logging of PII (User IDs, Emails, NIFs etc).

Data Sovereignty: Flags cloud configurations (AWS/Azure) that export data outside the EU.

✨ Magic Fix (Auto-Remediation)

Don't just find the bug—fix it.

One-Click Fix: Generates secure, refactored code snippets ready to copy-paste.

Educational Feedback: Explains why the code was insecure.

Executive Dashboard

Security Score: Real-time calculation of risk metrics based on AI findings.

Responsive Design: Enterprise-grade UI fully functional on Mobile and Desktop.

Multi-Language Report: Generates audits in English, Portuguese, Spanish, French, Italian, and German.

System Architecture

The project follows a distributed Microservices Architecture to ensure scalability and separation of concerns.

graph LR
    User[User / CI-CD] -- HTTP --> Front[Angular Frontend]
    Front -- REST API --> Back[Java Spring Boot]
    Back -- Internal API --> Engine[Python AI Engine]
    Engine -- Secure Request --> Gemini[Google Gemini 2.0]

   
Orchestration: Manages requests between Client and AI.

Smart Caching: Implements in-memory hashing to cache analysis results (reducing AI costs and latency to 0ms for repeated scans).

Resilience: WebFlux WebClient with timeouts and error handling.

AI Engine (Python Flask):

Prompt Engineering: Specialized personas for Security Auditing using Gemini 2.0.

Resilience: Handles Rate Limits (429) and API failures gracefully.

Universal Scanner: Language-agnostic analysis logic.

Techs

Frontend
Angular 17, TypeScript
Tailwind CSS (CDN), ngx-markdown, Responsive Layout
Backend
Java 17, Spring Boot 3
WebFlux, Maven, ConcurrentHashMap Cache
AI Engine
Python 3.10
Flask, Google GenAI SDK, Dotenv



Clone the repository:

git clone [https://github.com/silvatechf/codeguard-ai.git](https://github.com/silvatechf/codeguard-ai.git)
cd codeguard-ai


📸 Screenshots

(Add your screenshots here in the repository assets folder)

"The dashboard provides a clear, actionable report for non-technical auditors, bridging the gap between Legal (DPO) and Engineering."

🛡️ Security & Privacy

This tool follows Privacy by Design principles:

Stateless Analysis: Source code is processed in-memory and discarded immediately after analysis.

No PII Storage: We do not store user data, only the analysis metadata.

Secure Transport: All internal communication is designed to run within a private Docker network.

👤 Author

Fernando Silva
Software Engineer | Java & Angular Specialist | AI Enthusiast

© 2025 CodeGuard AI. All rights reserved.
