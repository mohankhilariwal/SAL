from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GOVERNED_RELEASE_", env_file=".env", extra="ignore"
    )

    env: str = "local"
    host: str = "127.0.0.1"
    api_port: int = 8000
    ui_port: int = 8501
    database_url: str = "sqlite:///./data/governed_release.db"
    data_dir: Path = Path("./data")
    generator: Literal["auto", "sdv", "fallback"] = "auto"
    model_gateway: Literal["stub", "ollama"] = "stub"
    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2:3b"
    policy_engine: Literal["python", "opa"] = "python"
    log_level: str = "INFO"
    max_rows: int = Field(default=5000, ge=1, le=100_000)
    max_runtime_seconds: int = Field(default=300, ge=10, le=3600)
    max_generation_retries: int = Field(default=2, ge=0, le=10)
    max_llm_requests: int = Field(default=4, ge=0, le=20)
    max_llm_characters: int = Field(default=12_000, ge=1000, le=100_000)
    privacy_exact_match_max: float = 0.002
    privacy_mean_similarity_max: float = 0.94
    privacy_rare_exposure_max: float = 0.15
    privacy_near_duplicate_rate_max: float = 0.02
    utility_score_min: float = 0.55

    @property
    def source_path(self) -> Path:
        return self.data_dir / "source" / "maplebridge_transactions.csv"

    def ensure_directories(self) -> None:
        for name in (
            "source",
            "candidate",
            "quarantine",
            "released/internal_sandbox",
            "released/named_external_partner",
            "evidence",
            "logs",
        ):
            (self.data_dir / name).mkdir(parents=True, exist_ok=True)
