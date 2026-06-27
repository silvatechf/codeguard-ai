"""
CodeGuard AI - Unified Router & Interface Controller
Exposes async endpoints with out-of-the-box type-safe checking via Django Ninja router mappings.
"""

from ninja import Router, NinjaAPI
from auditor.schemas import AuditRequestSchema, AuditResponseSchema  # Fixed absolute import path
from auditor.services import audit_engine_service

# Configuring global Django Ninja context orchestration
api = NinjaAPI(
    title="CodeGuard AI - Intelligence Enterprise Security Audit Engine",
    version="1.0.0",
    docs_url="/docs"
)

router = Router(tags=["Auditor Core Operations"])


@router.post("/analyze", response=AuditResponseSchema, summary="Evaluates source code payloads concurrently in-memory.")
async def analyze_code_endpoint(request, payload: AuditRequestSchema):
    """
    Ingests source code scripts, runs MD5 verification loops, matches signature telemetry data against 
    the OpenAI Structured parser, and updates metrics synchronously without disk operations.
    """
    response_data = await audit_engine_service.execute_audit(payload)
    return response_data


# Registering app specific routes to unified master core layout mapping
api.add_router("/auditor/", router)