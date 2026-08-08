# Stage 2B Technical Sources

**Verification date:** 2026-07-31.

The implementation remains vendor-neutral and local-first. The following primary or official sources informed the architecture; they do not imply that the tutorial implementation reproduces a vendor service.

1. Gordon V. Cormack, Charles L. A. Clarke and Stefan Buettcher, “Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods,” SIGIR 2009, DOI `10.1145/1571941.1572114`. Used for the rank-fusion option.
2. Nandan Thakur et al., “BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models,” 2021, `https://arxiv.org/abs/2104.08663`. Used to reinforce heterogeneous retrieval evaluation rather than one narrow benchmark.
3. Shahul Es et al., “RAGAs: Automated Evaluation of Retrieval Augmented Generation,” EACL 2024, DOI `10.18653/v1/2024.eacl-demo.16`. Used to separate retrieval quality, context quality and answer-generation quality.
4. NIST SP 800-207, “Zero Trust Architecture,” DOI `10.6028/NIST.SP.800-207`. Used for per-request authentication/authorization and policy enforcement close to the resource.
5. OWASP GenAI Security Project, “LLM01:2025 Prompt Injection,” `https://genai.owasp.org/llmrisk/llm01-prompt-injection/`. Used for the retrieved-content-as-untrusted-data rule.
6. Sentence Transformers documentation, “Cross-Encoders,” `https://sbert.net/examples/cross_encoder/applications/README.html`. Used to explain the candidate-generation/reranking trade-off and the production cross-encoder alternative.
7. Microsoft Learn, “Retrieval augmented generation (RAG) and indexes in Microsoft Foundry,” current page verified 2026-07-31, `https://learn.microsoft.com/en-us/azure/foundry/concepts/retrieval-augmented-generation`. Used as a current vendor example for retrieval-time access control, untrusted retrieved content, testing and cost/latency implications.
8. scikit-learn documentation, `TfidfVectorizer` and `TruncatedSVD`, verified 2026-07-31. Used for the standard TF-IDF/latent semantic analysis terminology; the tutorial code implements the minimum mathematics directly with NumPy to keep the local dependency surface small.

## Evidence-quality note

RRF is selected because it is deterministic, rank-based and does not require cross-channel score calibration. It is not presented as universally optimal. Research has shown that fusion behavior is workload-dependent; NorthStar therefore versions the fusion configuration and makes regression evaluation a rebuild gate.
