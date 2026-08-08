# Changelog

## 0.4.0 — 2026-07-31

- Added query-time authorization before candidate scoring or text exposure.
- Added BM25 lexical candidate generation.
- Added deterministic latent semantic candidate generation using TF-IDF + truncated SVD.
- Added reciprocal-rank fusion and metadata-aware reranking.
- Added overlap-aware evidence deduplication.
- Added exact citation construction and independent citation validation.
- Added retrieval context assembly that treats retrieved content as untrusted data.
- Added retrieval/RAG evaluation metrics, permission-boundary cases and regression tests.
- Updated all ten source-of-truth artefacts and the cumulative architecture to 0.4.0.
