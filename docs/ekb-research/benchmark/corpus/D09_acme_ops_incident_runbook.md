# Incident Runbook

Status: active
Date: 2026-06-27

Severity 1 incidents require an incident commander, communications lead, and
scribe. Customer-visible retrieval leaks are always Severity 1. The first action
is to freeze writes to the affected index_version, preserve trace_id evidence,
and disable any suspect grant until authorization is rechecked.

Post-incident reports must include the failed permission boundary and whether the
retrieval filter ran before ranking, after ranking, or both.
