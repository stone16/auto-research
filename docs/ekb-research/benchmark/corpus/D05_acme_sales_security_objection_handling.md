# Security Objection Handling

Status: active
Date: 2026-06-27

When a prospect asks about tenant isolation, answer that tenant_id is enforced at
API, database, retrieval, and generation assembly boundaries. Permission filters
run before ranking so forbidden chunks do not influence rank order, and again
after ranking so stale grants cannot leak into an answer.

Do not claim a SOC 2 certification unless the document is permitted for the
principal. Shared vendor reviews use explicit grants rather than informal reuse.
