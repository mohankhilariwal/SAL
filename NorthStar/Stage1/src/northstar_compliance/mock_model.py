from __future__ import annotations

import re

from .intake import Publication
from .model_gateway import ModelResult


class DeterministicMockSummaryModel:
    """Offline test double. It is not presented as an LLM quality substitute."""

    provider = "deterministic-mock"
    model = "stage1-rules-v1"

    _obligation = re.compile(r"\b(must|shall|required|prohibited|may not)\b", re.I)
    _deadline = re.compile(
        r"\b(within\s+\d+\s+(?:calendar\s+)?days|by\s+[A-Z][a-z]+\s+\d{1,2},\s+\d{4}|effective\s+[A-Z][a-z]+\s+\d{1,2},\s+\d{4})\b",
        re.I,
    )
    _area_terms = {
        "lending": ("credit", "lending", "loan", "adjudication"),
        "payments": ("payment", "screening", "transaction"),
        "customer-data": ("personal data", "customer data", "data sharing", "consent"),
    }

    def summarize(self, publication: Publication) -> ModelResult:
        facts: list[dict[str, object]] = []
        deadlines: list[dict[str, object]] = []
        areas: set[str] = set()
        for n, line in enumerate(publication.lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            low = stripped.lower()
            for area, terms in self._area_terms.items():
                if any(term in low for term in terms):
                    areas.add(area)
            if self._obligation.search(stripped):
                facts.append({
                    "statement": stripped,
                    "line_start": n,
                    "line_end": n,
                    "excerpt": stripped,
                    "uncertainty": "The text is source-derived; applicability to NorthStar is not assessed.",
                })
            for match in self._deadline.finditer(stripped):
                deadlines.append({
                    "text": match.group(0),
                    "line_start": n,
                    "line_end": n,
                    "excerpt": stripped,
                    "normalized_date": None,
                })
        if not facts:
            first = next((line.strip() for line in publication.lines if line.strip()), "No source fact found")
            line_num = next((i for i, line in enumerate(publication.lines, 1) if line.strip()), 1)
            facts.append({
                "statement": first,
                "line_start": line_num,
                "line_end": line_num,
                "excerpt": first,
                "uncertainty": "No explicit obligation keyword was detected by the offline test double.",
            })
        payload = {
            "executive_summary": (
                f"Preliminary source-bounded summary of {publication.metadata.title}. "
                f"{len(facts)} material statement(s) and {len(deadlines)} deadline candidate(s) were identified."
            ),
            "source_facts": facts[:12],
            "candidate_affected_areas": sorted(areas),
            "deadline_candidates": deadlines[:12],
            "missing_information": [
                "NorthStar policies, controls, processes and prior assessments were not provided.",
                "Legal applicability and jurisdiction-specific interpretation require qualified human review.",
            ],
            "uncertainties": [
                "The output is limited to the submitted publication.",
                "Candidate affected areas are keyword-based hypotheses, not accepted impact mappings.",
            ],
        }
        return ModelResult(
            provider=self.provider,
            model=self.model,
            payload=payload,
            usage={"input_bytes": publication.metadata.byte_count, "output_items": len(facts) + len(deadlines)},
        )
