"""Configuration for Socratic OpenClaw Skill."""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from socratic_core import SocratesConfig


class SocratiCOpenclawConfig(BaseModel):
    """Configuration for Socratic OpenClaw discovery skill."""

    # Socratic core config
    socratic_config: Optional[SocratesConfig] = Field(
        default=None,
        description="Socrates core configuration"
    )

    # Workspace settings
    workspace_root: Path = Field(
        default_factory=lambda: Path.home() / ".openclaw" / "workspace",
        description="Root workspace directory"
    )

    # LLM settings
    model: str = Field(
        default="claude-opus-4-5",
        description="LLM model to use"
    )
    temperature: float = Field(
        default=0.7,
        min=0.0,
        max=1.0,
        description="LLM temperature for creativity"
    )

    # Discovery settings
    max_questions: int = Field(
        default=8,
        description="Maximum number of discovery questions"
    )
    min_responses: int = Field(
        default=3,
        description="Minimum responses before allowing spec generation"
    )

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True

    def get_socratic_config(self) -> SocratesConfig:
        """Get or create Socrates config."""
        if self.socratic_config is None:
            self.socratic_config = SocratesConfig.from_env()
        return self.socratic_config

    def ensure_workspace(self) -> None:
        """Create workspace directories if they don't exist."""
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "projects").mkdir(exist_ok=True)
        (self.workspace_root / ".socrates-vectors").mkdir(exist_ok=True)
        (self.workspace_root / ".socrates-kb").mkdir(exist_ok=True)
