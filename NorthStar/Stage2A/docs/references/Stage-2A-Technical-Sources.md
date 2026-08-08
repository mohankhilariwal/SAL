# Stage 2A — Technical Sources

**Verification date:** 2026-07-31

The implementation is vendor-neutral and uses the Python standard library. These primary/authoritative references support the bounded technical choices; they do not turn the local tutorial store into a production control.

1. Python Software Foundation, **`hashlib` — Secure hashes and message digests**, Python 3.12 documentation. https://docs.python.org/3.12/library/hashlib.html
   - Used for SHA-256 source, metadata, version, chunk and manifest identities.
2. Python Software Foundation, **`os.replace`**, Python 3.12 documentation. https://docs.python.org/3.12/library/os.html#os.replace
   - Supports same-filesystem atomic replacement used after staging.
3. Python Software Foundation, **`pathlib` — Object-oriented filesystem paths**, Python 3.12 documentation. https://docs.python.org/3.12/library/pathlib.html
   - Used for bounded local path handling and artifact layout.
4. OWASP GenAI Security Project, **LLM01:2025 Prompt Injection**. https://genai.owasp.org/llmrisk/llm01-prompt-injection/
   - Supports treating retrieved/ingested content as untrusted data. S02A risk flags are diagnostic only.
5. NIST AI 600-1, **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile**, July 2024. https://doi.org/10.6028/NIST.AI.600-1
   - Supports provenance, governance and risk-management considerations for generative-AI systems.
6. NIST CAISI, **Strengthening AI Agent Hijacking Evaluations**, 2025-01-17. https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations
   - Reinforces the need to test instruction-bearing external content before later agent/tool use.

## Deferred reference

SQLite FTS5 documentation is recorded for S02B option analysis but is not used or claimed as implemented in S02A: https://sqlite.org/fts5.html
