terraform {
  required_version = ">= 1.7"
}

# Baseline placeholder only. Add approved providers, remote state, VPC Service
# Controls, service accounts, Cloud SQL/AlloyDB, locked Cloud Storage,
# Vertex AI Agent Engine/Cloud Run, Workflows and Cloud Operations.
locals {
  application = "governed-synthetic-data-release-agent"
  environment = "replace-me"
}
