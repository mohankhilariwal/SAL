terraform {
  required_version = ">= 1.7"
}

# Baseline placeholder only. Add approved providers, remote state, private
# endpoints, managed identities, PostgreSQL, immutable Blob Storage,
# Foundry Agent Service/Container Apps, Monitor and Durable Functions.
locals {
  application = "governed-synthetic-data-release-agent"
  environment = "replace-me"
}
