"""
Socratic OpenClaw Skill - Modern Architecture

Socratic method discovery skill for OpenClaw using socratic-core library.
This is the modernized replacement for the deprecated socrates-ai-openclaw package.

Usage:
    from socratic_openclaw_skill import SocraticDiscoverySkill

    skill = SocraticDiscoverySkill()
    result = await skill.start_discovery("My project idea")
    print(result["question"])
"""

from .skill import SocraticDiscoverySkill
from .config import SocraticOpenclawConfig

__version__ = "0.1.0"
__all__ = [
    "SocraticDiscoverySkill",
    "SocraticOpenclawConfig",
]
