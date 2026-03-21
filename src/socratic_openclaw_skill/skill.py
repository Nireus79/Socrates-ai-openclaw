"""Socratic Discovery Skill for OpenClaw."""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, List
from socratic_core import EventEmitter, EventType
from .config import SocraticOpenclawConfig


class SocraticDiscoverySkill:
    """Socratic method discovery skill for OpenClaw."""

    def __init__(self, config: Optional[SocraticOpenclawConfig] = None):
        """Initialize the discovery skill.

        Args:
            config: Configuration object. If None, creates default config.
        """
        self.config = config or SocraticOpenclawConfig()
        self.config.ensure_workspace()

        self.socratic_config = self.config.get_socratic_config()
        self.emitter = EventEmitter()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self._load_sessions()

    def _load_sessions(self) -> None:
        """Load sessions from storage."""
        sessions_file = self.config.workspace_root / ".socratic-sessions.json"
        if sessions_file.exists():
            try:
                with open(sessions_file, "r") as f:
                    self.sessions = json.load(f)
            except Exception:
                self.sessions = {}

    def _save_sessions(self) -> None:
        """Save sessions to storage."""
        sessions_file = self.config.workspace_root / ".socratic-sessions.json"
        with open(sessions_file, "w") as f:
            json.dump(self.sessions, f, indent=2)

    async def start_discovery(self, topic: str) -> Dict[str, Any]:
        """Start a new Socratic discovery session.

        Args:
            topic: The project or concept to discover

        Returns:
            Dictionary with session info and first question
        """
        session_id = f"discover_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"

        self.emitter.emit(
            EventType.SYSTEM_INITIALIZED,
            {"session_id": session_id, "topic": topic, "action": "discovery_started"},
        )

        # Initialize session
        self.sessions[session_id] = {
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "questions": [],
            "responses": [],
            "spec": None,
        }
        self._save_sessions()

        # Generate first question
        first_question = await self._generate_question(session_id, topic, [])

        self.sessions[session_id]["questions"].append(first_question)
        self._save_sessions()

        return {
            "status": "started",
            "session_id": session_id,
            "topic": topic,
            "question": first_question,
            "progress": {"step": 1, "responses": 0},
        }

    async def respond(self, session_id: str, response: str) -> Dict[str, Any]:
        """Record user response and get next question.

        Args:
            session_id: Session ID from start_discovery
            response: User's response to previous question

        Returns:
            Dictionary with next question or completion status
        """
        if session_id not in self.sessions:
            return {"status": "error", "message": f"Session {session_id} not found"}

        session = self.sessions[session_id]
        session["responses"].append(response)

        self.emitter.emit(
            EventType.AGENT_START,
            {"session_id": session_id, "step": len(session["responses"]), "response": response},
        )

        # Check if we have enough responses for spec generation
        if len(session["responses"]) >= self.config.min_responses:
            # Allow option to generate spec
            next_question = "Would you like to generate a specification? (yes/no)"
        elif len(session["responses"]) >= self.config.max_questions:
            # Force spec generation
            spec = await self._generate_spec(session_id)
            session["spec"] = spec
            self._save_sessions()

            return {
                "status": "spec_ready",
                "session_id": session_id,
                "message": "Specification generated. You can now download or refine it.",
            }
        else:
            # Generate next question
            next_question = await self._generate_question(
                session_id, session["topic"], session["responses"]
            )
            session["questions"].append(next_question)

        self._save_sessions()

        self.emitter.emit(
            EventType.AGENT_COMPLETE, {"session_id": session_id, "step": len(session["questions"])}
        )

        return {
            "status": "question_asked",
            "session_id": session_id,
            "question": next_question,
            "progress": {
                "questions_asked": len(session["questions"]),
                "responses_recorded": len(session["responses"]),
                "can_generate": len(session["responses"]) >= self.config.min_responses,
            },
        }

    async def generate(self, session_id: str) -> Dict[str, Any]:
        """Generate project specification from discovery.

        Args:
            session_id: Session ID from start_discovery

        Returns:
            Dictionary with generated specification and metadata
        """
        if session_id not in self.sessions:
            return {"status": "error", "message": f"Session {session_id} not found"}

        session = self.sessions[session_id]

        if len(session["responses"]) < self.config.min_responses:
            return {
                "status": "error",
                "message": f"Need at least {self.config.min_responses} responses to generate spec",
            }

        self.emitter.emit(
            EventType.AGENT_START, {"session_id": session_id, "action": "spec_generation"}
        )

        spec = await self._generate_spec(session_id)
        session["spec"] = spec

        # Save spec to workspace
        project_dir = (
            self.config.workspace_root / "projects" / self._sanitize_name(session["topic"])
        )
        project_dir.mkdir(parents=True, exist_ok=True)

        spec_file = project_dir / "PROJECT.md"
        with open(spec_file, "w") as f:
            f.write(spec)

        self._save_sessions()

        self.emitter.emit(
            EventType.AGENT_COMPLETE, {"session_id": session_id, "action": "spec_generation"}
        )

        return {
            "status": "spec_generated",
            "session_id": session_id,
            "spec": spec,
            "saved_to": str(spec_file),
            "artifacts": ["PROJECT.md"],
        }

    async def _generate_question(
        self, session_id: str, topic: str, previous_responses: List[str]
    ) -> str:
        """Generate next discovery question using Claude.

        Args:
            session_id: Current session ID
            topic: Project topic
            previous_responses: Previous user responses

        Returns:
            Next discovery question
        """
        # Simulated question generation
        # In real implementation, would call Claude API
        questions = [
            "What problem does this solve for your target users?",
            "Who is your primary target user?",
            "What are the key features needed?",
            "What's your timeline for the MVP?",
            "What are your technical constraints?",
            "How will you measure success?",
        ]

        step = len(previous_responses)
        if step < len(questions):
            return questions[step]
        return "Anything else important about this project?"

    async def _generate_spec(self, session_id: str) -> str:
        """Generate specification from discovery session.

        Args:
            session_id: Session ID

        Returns:
            Generated specification in Markdown format
        """
        session = self.sessions[session_id]

        # Simulated spec generation
        # In real implementation, would call Claude API
        spec = f"""# {session['topic']}

## Project Overview

Based on the discovery session conducted on {session['created_at']}, here is your project specification.

## Requirements

{chr(10).join(f'- {resp[:80]}...' if len(resp) > 80 else f'- {resp}' for resp in session['responses'][:3])}

## Architecture

The system will be built using modern technologies and best practices.

## Implementation Timeline

Phased approach:
1. Phase 1: Core features
2. Phase 2: Integration
3. Phase 3: Optimization

## Next Steps

1. Review this specification
2. Validate requirements
3. Begin implementation

---

Generated by Socratic OpenClaw Skill v0.1.0
"""
        return spec

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Sanitize project name for use in file paths."""
        return name.lower().replace(" ", "-")[:50]
