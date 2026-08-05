terraform {
  required_version = ">= 1.7"
}

# Baseline placeholder only. Add organization-approved providers, remote state,
# VPC endpoints, KMS keys, Aurora PostgreSQL, S3 versioning/Object Lock,
# AgentCore/ECS runtime, CloudWatch/OpenTelemetry and Step Functions callbacks.
locals {
  application = "governed-synthetic-data-release-agent"
  environment = "replace-me"
}
