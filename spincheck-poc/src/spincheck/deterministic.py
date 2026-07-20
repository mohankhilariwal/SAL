"""Deterministic linguistic layer (data plane, always on).

Every function here is pure, unit-testable, and injection-immune. spaCy is used
when installed; a regex sentencizer fallback keeps the POC runnable anywhere.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from .config import ControlPlane, injection_regexes

# optional deps -------------------------------------------------------------
try:  # pragma: no cover
    import spacy
    _NLP = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])
except Exception:  # noqa: BLE001
    _NLP = None

try:  # pragma: no cover
    from langdetect import detect_langs
except Exception:  # noqa: BLE001
    detect_langs = None


@dataclass
class Rejection:
    code: str
    message: str


@dataclass
class Features:
    text: str
    sentences: list[tuple[int, int]] = field(default_factory=list)
    quotes: list[tuple[int, int]] = field(default_factory=list)
    numeric_spans: list[tuple[int, int]] = field(default_factory=list)
    lexicon_hits: dict[str, list[tuple[int, int]]] = field(default_factory=dict)
    injection_spans: list[tuple[int, int]] = field(default_factory=list)
    rhetorical_questions: list[tuple[int, int]] = field(default_factory=list)
    language: str = "en"

    def summary(self) -> dict:
        g = lambda spans: [self.text[a:b] for a, b in spans][:8]  # noqa: E731
        return {
            "n_sentences": len(self.sentences),
            "quotes": g(self.quotes),
            "numeric_spans": g(self.numeric_spans),
            "lexicon_hits": {k: g(v) for k, v in self.lexicon_hits.items() if v},
            "injection_suspected": bool(self.injection_spans),
            "rhetorical_questions": g(self.rhetorical_questions),
        }


# ---------------------------------------------------------------- validation
_URL_ONLY = re.compile(r"^\s*(https?://\S+\s*)+$", re.I)


def validate_input(text: str, policy: dict) -> Rejection | None:
    p = policy["input"]
    if text is None or len(text.strip()) < p["min_chars"]:
        return Rejection("too_short", "Input is empty or too short to analyze.")
    if len(text) > p["max_chars"]:
        return Rejection("too_long", f"Input exceeds {p['max_chars']} characters.")
    if p.get("reject_url_only") and _URL_ONLY.match(text):
        return Rejection("url_only", "SpinCheck analyzes pasted text, not links — V1 does not open URLs.")
    return None


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    return text.replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")


def detect_language(text: str) -> str:
    if detect_langs is None:
        # heuristic fallback: ASCII-letter ratio
        letters = [c for c in text if c.isalpha()]
        if letters and sum(ord(c) < 128 for c in letters) / len(letters) < 0.7:
            return "unknown"
        return "en"
    try:
        best = detect_langs(text)[0]
        return best.lang if best.prob > 0.7 else "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


# ------------------------------------------------------------- segmentation
_SENT_FALLBACK = re.compile(r"[^.!?\n]+[.!?]?\s*")


def segment(text: str) -> list[tuple[int, int]]:
    if _NLP is not None:
        return [(s.start_char, s.end_char) for s in _NLP(text).sents]
    spans, i = [], 0
    for m in _SENT_FALLBACK.finditer(text):
        a, b = m.span()
        if text[a:b].strip():
            spans.append((a, b))
        i = b
    return spans or [(0, len(text))]


# ------------------------------------------------------------------- quotes
_QUOTE = re.compile(r'"([^"]{2,400})"')


def find_quotes(text: str) -> list[tuple[int, int]]:
    return [m.span(1) for m in _QUOTE.finditer(text)]


# ----------------------------------------------------------------- numerics
_NUM = re.compile(
    r"\b(\d[\d,.]*\s*(%|percent|million|billion|thousand|x|times)?"
    r"|twice|half|double|triple)\b", re.I)


def find_numeric(text: str) -> list[tuple[int, int]]:
    return [m.span() for m in _NUM.finditer(text) if m.group().strip()]


# ------------------------------------------------------------------ lexicons
def lexicon_hits(text: str, cp: ControlPlane) -> dict[str, list[tuple[int, int]]]:
    out: dict[str, list[tuple[int, int]]] = {}
    low = text.lower()
    for name, terms in cp.lexicons.items():
        if name == "injection_patterns":
            continue
        spans = []
        for t in terms:
            start = 0
            while True:
                i = low.find(t.lower(), start)
                if i < 0:
                    break
                # word-boundary guard
                before_ok = i == 0 or not low[i - 1].isalnum()
                after = i + len(t)
                after_ok = after >= len(low) or not low[after].isalnum()
                if before_ok and after_ok:
                    spans.append((i, after))
                start = i + 1
        if spans:
            out[name] = sorted(set(spans))
    return out


# ---------------------------------------------------------------- injection
def find_injection(text: str, cp: ControlPlane) -> list[tuple[int, int]]:
    return [m.span() for rx in injection_regexes(cp) for m in rx.finditer(text)]


_RHET_Q = re.compile(r"(how|why|who|what|when|isn't|aren't|don't)[^.?!]{5,120}\?", re.I)


def find_rhetorical_questions(text: str) -> list[tuple[int, int]]:
    return [m.span() for m in _RHET_Q.finditer(text)]


# ------------------------------------------------------------------ pipeline
def extract_features(text: str, cp: ControlPlane) -> Features:
    f = Features(text=text)
    f.language = detect_language(text)
    f.sentences = segment(text)
    f.quotes = find_quotes(text)
    f.numeric_spans = find_numeric(text)
    f.lexicon_hits = lexicon_hits(text, cp)
    f.injection_spans = find_injection(text, cp)
    f.rhetorical_questions = find_rhetorical_questions(text)
    return f
