# Architecture Decision Records

## ADR-001: Hybrid human-supervised autonomy

**Decision:** The user defines the objective and scope; the system independently performs bounded research tasks; humans approve scope-sensitive and final decisions. Approval checkpoints are configurable by project policy.

**Reason:** Preserve researcher authority while allowing meaningful autonomous investigation.

## ADR-002: Project memory plus shared knowledge

**Decision:** Support both project-scoped memory and workspace/institution-scoped shared knowledge.

**Guardrails:** No automatic promotion from project to shared scope. Enforce access filters before retrieval. Log publication, access and deletion events.

## ADR-003: Hybrid deployment

**Decision:** Develop locally with Docker; keep services portable to cloud or private infrastructure. Avoid hard dependencies on a single cloud provider or LLM vendor.

## ADR-004: Evidence-centred outputs

**Decision:** Substantive conclusions must be linked to source-backed evidence claims and precise locators where available. Record access level and provenance. Never fabricate citations or imply full-text access where only metadata/abstract was available.

## ADR-005: Modular domain expertise

**Decision:** Use a shared orchestration and provenance core with pluggable domain schemas, source connectors and appraisal rubrics.

**Reason:** Support multidisciplinary research without applying inappropriate one-size-fits-all quality criteria.
