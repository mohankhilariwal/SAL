# Stage 7B primary references — verified 2026-08-01

1. **NVIDIA AIPerf / NIM LLM benchmarking metrics.** Defines TTFT, end-to-end latency and ITL/TPOT; notes that TTFT includes queuing, prefill and network effects. https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html
2. **NVIDIA AIPerf sequence-length distributions.** Supports probability-weighted ISL/OSL pairs and variance for advanced benchmarking. https://docs.nvidia.com/aiperf/tutorials/datasets-inputs/sequence-length-distributions-for-advanced-benchmarking
3. **NVIDIA AIPerf load scheduling.** Distinguishes request rate from maximum concurrency and supports constant/Poisson-style load generation. https://docs.nvidia.com/aiperf/tutorials/load-patterns-scheduling/request-rate-with-max-concurrency
4. **vLLM bench serve.** Exposes request-rate, maximum-concurrency, input-length and output-length controls for online serving tests. https://docs.vllm.ai/en/stable/cli/bench/serve/
5. **vLLM benchmarking CLI guidance.** Describes load patterns for throughput, realistic, stress, latency and capacity testing. https://docs.vllm.ai/en/latest/benchmarking/cli/
6. **vLLM automatic prefix caching.** Explains KV-cache block reuse for shared prefixes; documentation updated 2026-06-23. https://docs.vllm.ai/en/stable/design/prefix_caching/
7. **MLCommons Agentic Inference for MLPerf Inference.** July 8, 2026 proposal for multi-turn, growing-context, closed-loop agentic inference benchmarking. https://mlcommons.org/2026/07/agentic-inference-for-mlperf-inference/
8. **MLCommons MLPerf Inference 5.1 small-LLM benchmark.** Separates prompt phase/TTFT from generation phase/TPOT and reports token throughput for variable-length workloads. https://mlcommons.org/2025/09/small-llm-inference-5-1/
9. **OpenTelemetry GenAI observability.** Describes GenAI token-usage and latency visibility; May 14, 2026. https://opentelemetry.io/blog/2026/genai-observability/
10. **NVIDIA GenAI-Perf documentation.** Documents metrics and states that GenAI-Perf is being phased out in favour of AIPerf. https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/genai-perf/README.html

These references inform definitions and benchmark method. None supplies NorthStar-specific performance numbers.
