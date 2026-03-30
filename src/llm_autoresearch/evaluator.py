from __future__ import annotations

import re

from .models import BenchmarkAnswer, BenchmarkItem, EvaluationDetail, EvaluationReport


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def evaluate_answers(
    benchmark: list[BenchmarkItem],
    answers: list[BenchmarkAnswer],
) -> EvaluationReport:
    answer_map = {answer.id: answer for answer in answers}
    details: list[EvaluationDetail] = []

    for item in benchmark:
        answer = answer_map.get(item.id, BenchmarkAnswer(id=item.id, answer="", citations=[]))
        normalized_answer = _normalize(answer.answer)
        citations = {citation.strip() for citation in answer.citations if citation.strip()}

        matched_must_include = [
            phrase for phrase in item.must_include if _normalize(phrase) in normalized_answer
        ]
        missing_must_include = [
            phrase for phrase in item.must_include if phrase not in matched_must_include
        ]
        matched_sources = [
            source_id for source_id in item.required_sources if source_id in citations
        ]
        missing_sources = [
            source_id for source_id in item.required_sources if source_id not in matched_sources
        ]

        if item.must_include:
            coverage_score = len(matched_must_include) / len(item.must_include)
        else:
            coverage_score = 1.0 if normalized_answer else 0.0

        if item.required_sources:
            citation_score = len(matched_sources) / len(item.required_sources)
        else:
            citation_score = 1.0

        score = round(0.75 * coverage_score + 0.25 * citation_score, 4)
        explanation = (
            f"coverage={coverage_score:.2f}, citations={citation_score:.2f}, "
            f"matched facts={len(matched_must_include)}/{len(item.must_include) or 1}"
        )
        details.append(
            EvaluationDetail(
                benchmark_id=item.id,
                score=score,
                coverage_score=round(coverage_score, 4),
                citation_score=round(citation_score, 4),
                matched_must_include=matched_must_include,
                matched_sources=matched_sources,
                missing_must_include=missing_must_include,
                missing_sources=missing_sources,
                explanation=explanation,
            )
        )

    total_score = round(sum(detail.score for detail in details) / len(details), 4) if details else 0.0
    return EvaluationReport(total_score=total_score, details=details)
