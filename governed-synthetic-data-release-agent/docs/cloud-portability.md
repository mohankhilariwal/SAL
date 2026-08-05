# Cloud portability

No cloud SDK is imported by domain or application code. The following are documented replacement examples, not deployed infrastructure.

## AWS example

- Agent/runtime: Amazon Bedrock AgentCore Runtime or ECS/Fargate.
- Tool and invocation boundary: AgentCore Gateway and Policy, or API Gateway plus a separately administered PDP.
- Database: Amazon Aurora PostgreSQL.
- Candidate/evidence/export: Amazon S3 with versioning, encryption and Object Lock where appropriate.
- Approval orchestration: AWS Step Functions callback pattern.
- Identity: IAM Identity Center/Cognito for users and IAM roles/workload identity for services.
- Model: Amazon Bedrock through the existing model-gateway port.
- Observability: OpenTelemetry to AgentCore Observability/CloudWatch; immutable evidence in a segregated S3 account/bucket.

## Google Cloud example

- Agent/runtime: Vertex AI Agent Engine or Cloud Run/GKE for the existing container.
- Database: Cloud SQL for PostgreSQL or AlloyDB.
- Candidate/evidence/export: Cloud Storage with retention policy, object versioning and bucket lock where required.
- Approval orchestration: Workflows with callback endpoint or a durable event-driven service.
- Identity: Cloud Identity/Workforce Identity Federation and service accounts.
- Model: Vertex AI through the model-gateway port.
- Observability: Cloud Logging, Monitoring and Trace with OpenTelemetry export.

## Azure example

- Agent/runtime: Microsoft Foundry Agent Service hosted agent or Azure Container Apps/AKS.
- Database: Azure Database for PostgreSQL.
- Candidate/evidence/export: Blob Storage with versioning and immutable storage policies.
- Approval orchestration: Durable Functions or Logic Apps callback workflow.
- Identity: Microsoft Entra ID and managed identities.
- Model: Foundry Models/Azure OpenAI through the model-gateway port.
- Observability: Azure Monitor/Application Insights with OpenTelemetry.

Before selecting a managed agent runtime, verify regional availability, data residency, preview/GA status, identity capabilities, network isolation, policy enforcement, evidence export and pricing for the deployment date.
