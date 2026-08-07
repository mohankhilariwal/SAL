"""Machine-readable Stage 0 constitution constants.

This module deliberately contains no model, agent, tool, retrieval or runtime
implementation. It centralizes stable repository facts used by validation.
"""

from pathlib import Path

REPOSITORY_NAME = "northstar-agentic-compliance"
ARCHITECTURE_VERSION = "0.1.0"
REPOSITORY_VERSION = "0.1.0"
HANDOFF_VERSION = "0.1.0"
PYTHON_BASELINE = "3.13"

SOURCE_OF_TRUTH_DIRECTORY = Path("docs/source-of-truth")
SOURCE_OF_TRUTH_FILES = (
    "00-Project-Constitution.md",
    "01-Business-and-User-Story-Baseline.md",
    "02-Requirements-Register.md",
    "03-Architecture-Baseline.md",
    "04-Component-and-Agent-Catalogue.md",
    "05-Data-and-Schema-Register.md",
    "06-ADR-Register.md",
    "07-Repository-Manifest.md",
    "08-Risk-Assumption-and-Issue-Register.md",
    "09-Stage-Handoff-Pack.md",
)

REQUIRED_HANDOFF_HEADINGS = (
    "## A. Stage completed",
    "## B. Capabilities now available",
    "## C. Accepted architecture decisions",
    "## D. Current component inventory",
    "## E. Current agent inventory",
    "## F. Current data and state objects",
    "## G. Current interfaces and tools",
    "## H. Repository state",
    "## I. Tests completed",
    "## J. Known limitations",
    "## K. Open risks, assumptions and issues",
    "## L. Compatibility constraints",
    "## M. Required input for the next stage",
    "## N. Next architectural problem",
    "## O. Exact continuation instruction",
)

REQUIRED_STAGE_HEADINGS = tuple(f"## {number}." for number in range(1, 28))

IDENTIFIER_PATTERN = (
    r"\b(?:AP|SG|BSC|US|FR|NFR|CMP|AGT|TOOL|DATA|INT|POL|RSK|CTL|EVAL|ADR|TEST|ASM|ISS)-\d{3}\b"
)
