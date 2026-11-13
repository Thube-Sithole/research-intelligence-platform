# Architecture baseline

## 1. System boundaries

- **Frontend:** research workspace, project navigation, evidence inspection, approval and report review.
- **API/application:** identity, project membership, research-run lifecycle, policy enforcement and orchestration entry points.
- **Orchestration:** LangGraph state machine. Agents are bounded workers, not independent authorities.
- **Evidence services:** source discovery, document ingestion, extraction, provenance, deduplication and appraisal.
- **Persistence:** relational records for projects/runs/sources/claims/events; vector index for retrieval; object storage for original files and parsed artifacts.

## 2. Research run lifecycle

`draft -> planning -> awaiting_scope_approval -> discovery -> extraction -> appraisal -> analysis -> critique -> (gap_search -> discovery)* -> awaiting_final_review -> report_ready`

A run may also end in `cancelled`, `failed` or `blocked`. Each transition should create an immutable workflow event. Human approval is a first-class state transition and must be attributable to an authenticated user.

## 3. Shared and project memory

Memory records include `scope_type`, `scope_id`, `owner_workspace_id`, `visibility`, `created_by`, `source_id`, `created_at` and retention metadata. Retrieval queries must constrain workspace, project membership and visibility before vector ranking. Shared-memory publication requires explicit approval and audit logging. Never use a global vector search and filter permissions only after returning results to an agent.

## 4. Evidence provenance

A source record should capture canonical identifier (DOI, PMID, OpenAlex ID, URL or upload ID), title, authors, publication date, retrieval timestamp, provider, licence/access status, content type and content hash. Evidence claims should capture exact quotation or faithful structured extraction, page/section/table/figure locator, extraction method, model version, source-content hash and confidence/uncertainty metadata. Abstract-only evidence must remain labelled as abstract-only.

## 5. Domain modules

Domain modules supply schemas, terminology, source adapters, inclusion criteria and appraisal rubrics. They must not change core provenance or access-control rules. Initial modules: general, medical/biomedical, engineering, science, AI/technology and business/economics.

## 6. Security and governance

Authentication and project-level authorisation are required before multi-user deployment. Use least-privilege service credentials, secrets outside source control, encrypted transport/storage, retention controls, audit events and prompt-injection isolation for retrieved documents. Treat all source text as untrusted data, never as instructions to agents.

## 7. Reliability and evaluation

Maintain a versioned evaluation set covering retrieval relevance, recall of key evidence, extraction fidelity, citation/locator correctness, contradiction detection, unsupported-claim rate, domain-rubric agreement and run reproducibility. Report uncertainty and abstain when evidence is insufficient.
