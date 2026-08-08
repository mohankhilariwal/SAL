# Stage 4B Technical Sources

Verified 2026-07-31. Primary documentation only.

1. Temporal, “Human-in-the-Loop AI Agent” and workflow/external-interaction documentation: https://docs.temporal.io/ai-cookbook/human-in-the-loop-python and https://docs.temporal.io/design-patterns/external-interaction-patterns
2. AWS Step Functions, callback tasks and human approval: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html and https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-human-approval.html
3. Microsoft Durable Task, human interaction pattern: https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-human-interaction
4. Google Cloud Workflows callbacks: https://docs.cloud.google.com/workflows/docs/creating-callback-endpoints
5. LangGraph interrupts and persistence: https://docs.langchain.com/oss/python/langgraph/interrupts and https://docs.langchain.com/oss/python/langgraph/persistence
6. SQLite transactions, isolation and WAL: https://sqlite.org/isolation.html and https://sqlite.org/wal.html

The local implementation is NorthStar-specific. Vendor documentation is used for option comparison, not to claim equivalent managed-service guarantees.
