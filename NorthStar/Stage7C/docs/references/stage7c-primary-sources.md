# Stage 7C Primary Sources

Verified 2026-08-01. Sources are used as technical evidence, not as proof that a capability is enabled in NorthStar.

- **R1 — Leviathan, Kalman and Matias, “Fast Inference from Transformers via Speculative Decoding.”** Original lossless speculative-decoding algorithm. https://arxiv.org/abs/2211.17192
- **R2 — Chen et al., “Accelerating Large Language Model Decoding with Speculative Sampling.”** Modified rejection sampling preserving the target distribution within hardware numerics. https://arxiv.org/abs/2302.01318
- **R3 — vLLM, Automatic Prefix Caching.** Exact shared-prefix KV reuse; benefits prefill and does not reduce decode work. https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
- **R4 — vLLM, Speculative Decoding.** Documents medium-to-low-QPS, memory-bound suitability and recommends reproducible benchmarking. https://docs.vllm.ai/en/latest/features/spec_decode/
- **R5 — SGLang documentation.** RadixAttention/prefix caching, serving performance and multi-GPU capabilities. https://docs.sglang.ai/
- **R6 — SGLang, PD Disaggregation.** Separates compute-intensive prefill and memory-intensive decode; included as an advanced deferred option. https://docs.sglang.ai/advanced_features/pd_disaggregation.html
- **R7 — NVIDIA TensorRT-LLM overview.** Paged KV cache, chunked prefill and EAGLE/MTP/NGram speculative methods. https://nvidia.github.io/TensorRT-LLM/overview.html
- **R8 — NVIDIA TensorRT-LLM, Speculative Sampling.** Conditions under which draft/verify can reduce latency and supported technique families. https://nvidia.github.io/TensorRT-LLM/advanced/speculative-decoding.html
- **R9 — NVIDIA TensorRT-LLM, KV Cache Reuse.** Reuse of pages for requests with the same prompt and effect on TTFT. https://nvidia.github.io/TensorRT-LLM/advanced/kv-cache-reuse.html
- **R10 — NVIDIA TensorRT-LLM, Quantization.** Weight and KV-cache quantization controls. https://nvidia.github.io/TensorRT-LLM/latest/features/quantization.html
- **R11 — Hugging Face Transformers, Generation Strategies.** Assisted decoding, prompt lookup and self-speculative variants. https://huggingface.co/docs/transformers/en/generation_strategies
- **R12 — Cai et al., “Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads.”** Multiple auxiliary heads and tree verification. https://arxiv.org/abs/2401.10774
- **R13 — Liu et al., “Speculative Decoding: Performance or Illusion?”** 2026 preprint emphasizing batch-, workload- and verification-dependent performance. https://arxiv.org/abs/2601.11580
- **R14 — Amazon Bedrock, Prompt Caching.** Managed prompt-cache checkpoints and cache-key concepts. https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- **R15 — Google Cloud Vertex AI, Context Cache samples.** Managed context-cache lifecycle examples. https://docs.cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-create-context-cache

## Evidence interpretation

1. Research papers establish algorithmic claims under their experimental conditions; they do not establish NorthStar production performance.
2. Runtime documentation identifies currently supported capability categories; exact API and compatibility must be reverified when a runtime is selected.
3. Vendor benchmark claims are not copied into NorthStar capacity or cost records.
4. Stage 7C local results are `simulated`; no GPU endpoint was executed.
