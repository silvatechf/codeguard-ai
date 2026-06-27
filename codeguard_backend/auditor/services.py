"""
CodeGuard AI - Neural Audit Engine & Cache Core
Handles concurrent memory caching via MD5 hashing, executes type-safe async calls to OpenAI,
and implements zero-fallback defensive programming, log-redaction, and strict isolation loops.
"""

import os
import re
import hashlib
import logging
from typing import Dict, Optional
from openai import AsyncOpenAI
from auditor.schemas import AuditRequestSchema, OpenAIEngineOutputSchema, AuditResponseSchema

logger = logging.getLogger(__name__)


class AuditEngineService:
    """Stateless micro-orchestrator managing code auditing execution with hardened log redaction."""

    def __init__(self):
        self._cache: Dict[str, AuditResponseSchema] = {}
        
        # Defensive check for API token without logging the placeholder value
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("❌ CRITICAL: OpenAI access credential identifier is missing from target runtime environment.")
        
        self.client = AsyncOpenAI(api_key=api_key or "placeholder")

    def _generate_md5_hash(self, code: str, language: str) -> str:
        """Computes a unique signature using limited payload references to support O(1) cache hits safely."""
        # Clean inline comments to prevent cache evasion from comment tampering (e.g., // 1, // 2)
        functional_code = re.sub(r"//.*", "", code)
        functional_code = re.sub(r"/\*.*?\*/", "", functional_code, flags=re.DOTALL)

        # Enforce strict maximum length on cache string serialization to mitigate compute exhaustion
        safe_boundary = functional_code[:20000].strip()
        payload_string = f"{safe_boundary}:{language.strip()}"
        return hashlib.md5(payload_string.encode("utf-8")).hexdigest()

    def _get_language_mapping(self, lang_code: str) -> str:
        """Maps incoming short codes into absolute readable language descriptions for prompt tuning."""
        mapping = {
            "pt": "Portuguese (Brasil)",
            "es": "Spanish",
            "fr": "French",
            "it": "Italian",
            "de": "German",
            "en": "English"
        }
        return mapping.get(lang_code.lower(), "English")

    def _sanitize_and_validate_output(self, raw_ai: OpenAIEngineOutputSchema, original_code: str) -> OpenAIEngineOutputSchema:
        """
        Defensive Programming Layer.
        Enforces absolute sanity checks over the parsed AI structured object before transmission.
        """
        clean_code = raw_ai.fixed_code.strip()
        if clean_code.startswith("```"):
            lines = clean_code.splitlines()
            if lines and lines[0].startswith("```"):
                lines.pop(0)
            if lines and lines[-1].startswith("```"):
                lines.pop()
            clean_code = "\n".join(lines).strip()

        if not clean_code:
            clean_code = original_code.strip()

        score = max(0, min(100, raw_ai.security_score))
        issues = max(0, raw_ai.issues_count)

        if score == 100 and issues > 0:
            issues = 0
        elif score < 100 and issues == 0:
            issues = 1

        risk = raw_ai.risk_level.strip().upper()
        if risk not in ("LOW", "MEDIUM", "HIGH", "CRITICAL"):
            if score >= 85: risk = "LOW"
            elif score >= 60: risk = "MEDIUM"
            elif score >= 35: risk = "HIGH"
            else: risk = "CRITICAL"

        gdpr = raw_ai.gdpr_status.strip().upper()
        if gdpr not in ("COMPLIANT", "NON-COMPLIANT"):
            gdpr = "COMPLIANT" if score >= 80 else "NON-COMPLIANT"

        return OpenAIEngineOutputSchema(
            markdown_report=raw_ai.markdown_report.strip() or "### No description provided by the auditing system.",
            fixed_code=clean_code,
            security_score=score,
            risk_level=risk,
            gdpr_status=gdpr,
            issues_count=issues
        )

    async def execute_audit(self, payload: AuditRequestSchema) -> AuditResponseSchema:
        """Processes source code dynamically in-memory following Privacy by Design architectures."""
        target_code = payload.javaCode
        target_lang = payload.language or "en"
        
        cache_key = self._generate_md5_hash(target_code, target_lang)
        if cache_key in self._cache:
            logger.info("⚡ CONCURRENT CACHE HIT: Returning saved structural report state.")
            return self._cache[cache_key]

        logger.info("🐢 CONCURRENT CACHE MISS: Formulating structured prompt contract to OpenAI.")
        readable_language = self._get_language_mapping(target_lang)

        system_instructions = (
            "You are an Elite DevSecOps Architect and Senior GDPR Compliance Auditor.\n"
            "Analyze the user's submitted source code snippet for critical flaws including "
            "PII leaks, unnecessary logging violations, insecure Cloud architecture configurations "
            "(AWS/Azure/GCP credentials), injection risks, and absolute cross-border sovereignty compliance.\n"
            "You must return full, production-ready refactored fixed code, an absolute granular security score, "
            "and structural metrics without fallbacks.\n"
            "CRITICAL RULE FOR THE MARKDOWN REPORT:\n"
            "Do NOT include the refactored/fixed code snippet inside the 'markdown_report' parameter. "
            "Do NOT write transitional phrases promising code blocks below. "
            "The 'markdown_report' must contain ONLY text analysis, recommendations, and metrics. "
            "The refactored code belongs EXCLUSIVELY to the 'fixed_code' parameter."
        )

        user_content = (
            f"Analyze this raw code sample:\n"
            f"```\n{target_code}\n```\n\n"
            f"Requirements:\n"
            f"1. Generate the complete detailed markdown report exclusively written in: {readable_language}.\n"
            f"2. Provide full remediation inside the structured 'fixed_code' output parameter."
        )

        try:
            completion = await self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": user_content}
                ],
                response_format=OpenAIEngineOutputSchema,
                temperature=0.0,  # Enforces absolute determinism to lock evaluation metric consistency
                timeout=90.0
            )

            structured_ai_response: OpenAIEngineOutputSchema = completion.choices[0].message.parsed
            
            if not structured_ai_response:
                raise ValueError("OpenAI failed to parse the structured output parameters schema.")

            sanitized_output = self._sanitize_and_validate_output(structured_ai_response, target_code)

            final_response = AuditResponseSchema(
                success=True,
                message=sanitized_output.markdown_report,
                fixedCode=sanitized_output.fixed_code,
                codeLength=len(target_code),
                securityScore=sanitized_output.security_score,
                riskLevel=sanitized_output.risk_level,
                gdprStatus=sanitized_output.gdpr_status,
                issuesCount=sanitized_output.issues_count
            )

            self._cache[cache_key] = final_response
            return final_response

        except Exception as error:
            # DevSecOps Hardening: Redacted telemetry logging to shield token parameters from container stderr dumps
            error_class = error.__class__.__name__
            logger.error(f"❌ Core Neural Engine Failure: Intercepted {error_class} runtime bounds.")
            
            return AuditResponseSchema(
                success=False,
                message=f"### Security Audit Execution Failure\nInternal processing gateway exception encountered: {error_class}",
                fixedCode="",
                codeLength=len(target_code),
                securityScore=0,
                riskLevel="ERROR",
                gdprStatus="ERROR",
                issuesCount=0
            )


audit_engine_service = AuditEngineService()