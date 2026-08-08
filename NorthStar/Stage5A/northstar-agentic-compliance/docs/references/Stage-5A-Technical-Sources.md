# Stage 5A Technical Sources

**Verification date:** 2026-08-01

The implementation remains vendor-neutral and standard-library-only. These primary sources support the specification, schema, lifecycle and control principles; they do not imply production conformance.

1. **JSON Schema, Draft 2020-12 Specification** — structural schema vocabulary and validation model.  
   https://json-schema.org/draft/2020-12
2. **JSON Schema Validation: A Vocabulary for Structural Validation** — validation keywords and annotation/assertion behavior.  
   https://json-schema.org/draft/2020-12/json-schema-validation
3. **NIST AI Risk Management Framework (AI RMF 1.0)** — governance, mapping, measurement and management of AI risk.  
   https://www.nist.gov/itl/ai-risk-management-framework
4. **NIST AI RMF Playbook** — voluntary actions for intended purpose, risk tolerance, documentation, monitoring and lifecycle governance.  
   https://airc.nist.gov/airmf-resources/playbook/
5. **NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1** — secure development practices and evidence expectations.  
   https://csrc.nist.gov/pubs/sp/800/218/final
6. **OpenAI, A Practical Guide to Building Agents** — agent instructions, tools, orchestration and guardrail concepts; used only as a representative vendor mapping.  
   https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
7. **OpenAI Agents SDK — Guardrails and Human-in-the-Loop** — representative SDK-level guardrail and approval concepts; not used by the local code.  
   https://openai.github.io/openai-agents-python/guardrails/  
   https://openai.github.io/openai-agents-python/human_in_the_loop/
8. **Stage 4C Agent Harness Engineering and Handoff Pack** — authoritative local baseline for accepted IDs, versions, authority and deferred capabilities. Stored in `docs/baseline/Stage-4C-Handoff-Pack-supplied.md` and the project source package.

## Evidence classification

- JSON Schema and NIST sources describe established standards/guidance.
- SDK/documentation sources are vendor-specific mappings and rapidly changing.
- NorthStar's specification model, identifiers, decision matrices and local benchmark results are tutorial architecture decisions and local evidence, not industry standards.
