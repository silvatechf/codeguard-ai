"""
CodeGuard AI - Data Validation Schemas
Defines structured contracts for incoming requests with enterprise payload size guardrails.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AuditRequestSchema(BaseModel):
    """Payload schema expected from the Angular frontend with defensive limits."""
    # Enforces a strict minimum of 10 characters and a maximum ceiling of 60,000 characters
    javaCode: str = Field(..., min_length=10, max_length=60000, description="The raw source code content to evaluate.")
    language: Optional[str] = Field("en", description="ISO language code for the markdown evaluation report.")

    @field_validator("javaCode")
    @classmethod
    def validate_code_payload_safety(cls, value: str) -> str:
        """Defensive programming validation to drop abnormally large execution blocks before LLM call."""
        if len(value) > 55000:
            raise ValueError("The submitted code package exceeds the enterprise tier auditing safety limit.")
        return value


class OpenAIEngineOutputSchema(BaseModel):
    """Strict structural mapping used by OpenAI Structured Outputs."""
    markdown_report: str = Field(..., description="Comprehensive vulnerability report styled in high-fidelity markdown layout.")
    fixed_code: str = Field(..., description="Completely refactored, secure, production-ready implementation of the input code.")
    security_score: int = Field(..., ge=0, le=100, description="Absolute risk metric integer calibrated strictly between 0 and 100.")
    risk_level: str = Field(..., description="Must evaluate specifically to one of: 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'.")
    gdpr_status: str = Field(..., description="Must evaluate specifically to one of: 'COMPLIANT', 'NON-COMPLIANT'.")
    issues_count: int = Field(..., ge=0, description="Actual physical count of security flaws detected in the codebase.")


class AuditResponseSchema(BaseModel):
    """Unified type-safe response schema emitted by the Django Ninja API."""
    success: bool
    message: str
    fixedCode: Optional[str] = None
    codeLength: int
    securityScore: int
    riskLevel: str
    gdprStatus: str
    issuesCount: int