# Stage 7A Primary References

Verified 2026-08-01. The architecture is vendor-neutral; these sources inform option behavior and limitations rather than selecting a product.

1. Python Software Foundation, *asyncio — Asynchronous I/O*, Python documentation. https://docs.python.org/3/library/asyncio.html
2. Python Software Foundation, *Coroutines and Tasks* (`TaskGroup`, cancellation and timeout), Python documentation. https://docs.python.org/3/library/asyncio-task.html
3. Python Software Foundation, *Synchronization Primitives* (`Semaphore`, `BoundedSemaphore`), Python documentation. https://docs.python.org/3/library/asyncio-sync.html
4. Python Software Foundation, *Queues* (`asyncio.Queue` and finite `maxsize`), Python documentation. https://docs.python.org/3/library/asyncio-queue.html
5. Amazon Web Services, *Amazon SQS standard queues* and *at-least-once delivery*. https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues.html
6. Apache Kafka, *Introduction and ordering within a topic partition*. https://kafka.apache.org/documentation/
7. RabbitMQ, *Consumer acknowledgements and publisher confirms*; *Quorum queues*. https://www.rabbitmq.com/docs/confirms and https://www.rabbitmq.com/docs/quorum-queues
8. Temporal Technologies, *Workflow Execution*, *Activity Execution* and event-history replay. https://docs.temporal.io/workflow-execution and https://docs.temporal.io/activity-execution
9. Celery Project, *Tasks* and idempotency guidance. https://docs.celeryq.dev/en/stable/userguide/tasks.html

## Source-derived engineering points

- Python `asyncio` supplies coroutine, task, timeout, queue and semaphore primitives suitable for the local I/O-bound reference.
- Standard distributed queues can redeliver or reorder messages, so application idempotency and explicit ordering scope remain necessary.
- Durable workflow engines add event history and replay but impose their own determinism, lifecycle and operational model.
- Task frameworks recommend idempotent task behavior where retries or late acknowledgements may cause re-execution.
