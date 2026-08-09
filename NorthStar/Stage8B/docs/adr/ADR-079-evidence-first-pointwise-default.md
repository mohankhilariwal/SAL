# ADR-079 - Evidence-first, criterion-isolated, score-last pointwise default

**Status:** Accepted

**Decision:** Use pointwise evaluation as the default. Evaluate unidimensional criteria independently, record evidence and missing information, then emit verdict/score. Pairwise comparisons require candidate anonymization and order swapping; listwise evaluation is diagnostic only.
