# ADR 0001: Hexagonal architecture

**Status:** Accepted

Keep domain/application logic independent of presentation, persistence, local files, SDV, Ollama, OPA and cloud services. Use typed ports and replaceable adapters. This increases file count but prevents production migration from rewriting policy and workflow rules.
