# Stage 8A Primary Sources

Verified on 2026-08-01 unless otherwise noted.

1. **[R1] NIST AI RMF Core and Playbook — Measure.** Requires documented test sets, metrics, TEVV tools, deployment-context similarity, domain-expert input and production monitoring. https://airc.nist.gov/airmf-resources/playbook/measure/
2. **[R2] NIST AI RMF Core.** Measure 1.3 and Measure 2.1–2.4 establish independent assessment, documented test sets/metrics, representative conditions and production monitoring. https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
3. **[R3] Anthropic, “Demystifying evals for AI agents,” 2026-01-09.** Defines tasks, trials, graders, transcripts, outcomes, evaluation harnesses and suites; recommends mixed graders, multiple trials, isolated environments, transcript review, balanced datasets and capability/regression separation. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
4. **[R4] OpenAI Evals API reference.** Defines evaluation structures, data-source schemas, graders and repeatable runs across model configurations. https://platform.openai.com/docs/api-reference/evals
5. **[R5] OpenAI Evals, “Building an eval.”** Describes datasets, eval classes, split/version naming and meta-evaluation of model-graded evaluators. https://github.com/openai/evals/blob/main/docs/build-eval.md
6. **[R6] Gebru et al., “Datasheets for Datasets,” CACM 2021.** Proposes structured documentation of motivation, composition, collection, intended use and limitations. https://arxiv.org/abs/1803.09010
7. **[R7] Pushkarna et al., “Data Cards,” ACM FAccT 2022.** Treats dataset documentation as a stakeholder-facing lifecycle product recording origins, evolution, intended use and ethical considerations. https://research.google/pubs/data-cards-purposeful-and-transparent-dataset-documentation-for-responsible-ai/
8. **[R8] Liang et al., “Holistic Evaluation of Language Models,” TMLR 2023.** Advocates broad scenario coverage, explicit incompleteness and multi-metric evaluation under standardized conditions. https://arxiv.org/abs/2211.09110
9. **[R9] Es et al., “RAGAs,” EACL 2024.** Separates retrieval relevance, answer faithfulness and answer quality; useful as a taxonomy, not as automatic ground truth. https://aclanthology.org/2024.eacl-demo.16/
10. **[R10] Saad-Falcon et al., “ARES,” NAACL 2024.** Combines synthetic data, lightweight judges and a small human-labelled set; illustrates why judge calibration and domain shift matter. https://aclanthology.org/2024.naacl-long.20/
11. **[R11] Liu et al., “AgentBench,” 2023.** Evaluates agents in multi-turn interactive environments and identifies long-horizon reasoning, decision-making and instruction-following failures. https://arxiv.org/abs/2308.03688
12. **[R12] Mialon et al., “GAIA,” 2023.** Uses real-world tasks requiring reasoning, tool use and multiple capabilities, with held-back answers for leaderboard integrity. https://arxiv.org/abs/2311.12983
13. **[R13] Yao et al., “tau-bench,” 2024.** Grades end-state outcomes in tool-agent-user interactions and introduces pass^k to quantify reliable repeated success. https://arxiv.org/abs/2406.12045
14. **[R14] Deng et al., “Investigating Data Contamination in Modern Benchmarks,” NAACL 2024.** Shows contamination can inflate benchmark results and proposes contamination-detection protocols. https://aclanthology.org/2024.naacl-long.482/
15. **[R15] Choi et al., “How Contaminated Is Your Benchmark?,” ICML 2025.** Presents a contamination measure and reinforces the need to treat benchmark leakage as an evaluation-validity risk. https://proceedings.mlr.press/v267/choi25b.html
16. **[R16] Sun et al., “The Emperor’s New Clothes in Benchmarking?,” ICML 2025.** Finds that common benchmark-update strategies do not reliably balance semantic fidelity and contamination resistance. https://proceedings.mlr.press/v267/sun25t.html
17. **[R17] Anthropic evaluation guidance on multiple trials.** The 2026 article distinguishes pass@k from pass^k and emphasizes stable isolated environments; NorthStar uses repeated deterministic local trials only as harness evidence, not production reliability evidence. Same source as [R3].
18. **[R18] NIST AI Resource Center.** Provides TEVV resources and notes that AI RMF 1.0 is under revision; NorthStar treats current guidance as voluntary and reviewable, not a legal conclusion. https://airc.nist.gov/
