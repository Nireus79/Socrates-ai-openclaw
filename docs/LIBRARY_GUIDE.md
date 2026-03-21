# socrates-ai-openclaw Library Guide

## Overview

**socrates-ai-openclaw** is a framework integration that implements Socratic discovery sessions using the OpenClaw framework. It provides a skill-based approach to guided questioning, knowledge management, and specification generation.

**Current Version**: 0.1.0
**Package Name**: `socrates-ai-openclaw`
**Python Support**: 3.8+
**License**: MIT
**Status**: Production Ready
**Note**: Replaces deprecated `socratic-openclaw-skill` package

## What This Library Does

socrates-ai-openclaw provides:

### 1. Socratic Discovery Sessions
- Multi-turn guided questioning
- Adaptive question generation based on responses
- Session state management and persistence
- Resumable discovery sessions
- Question history and context tracking

### 2. Knowledge Base Integration
- ChromaDB vector store for knowledge retrieval
- Sentence transformers for embeddings
- RAG-powered context insertion
- Document chunking and indexing
- Similarity search for relevant context

### 3. Specification Generation
- Auto-generate specifications from discovery sessions
- Extract requirements from questions and answers
- Create technical documentation
- Export specifications in multiple formats

### 4. Session Management
- Create and manage discovery sessions
- Store session state to JSON files
- Resume interrupted sessions
- Session analytics and reporting

### 5. Configuration Management
- Environment-based configuration
- API key management
- Model selection (Claude versions)
- Customizable prompts and templates

## Architecture

```
socrates-ai-openclaw
    │
    ├── skill.py         # Main SocraticDiscoverySkill class
    ├── config.py        # Configuration management
    ├── sessions/        # Session storage
    └── __init__.py      # Public API exports
```

## Key Classes

### SocraticDiscoverySkill
Main class for managing discovery sessions:

```python
from socrates_ai_openclaw import SocraticDiscoverySkill

skill = SocraticDiscoverySkill(
    api_key="sk-...",
    model="claude-3-5-sonnet-20241022",
    knowledge_base_path="/data/knowledge"
)
```

### Session Management
```python
from socrates_ai_openclaw import SocraticDiscoverySkill

skill = SocraticDiscoverySkill()

# Start discovery
session = await skill.start_discovery(
    topic="Building a REST API",
    initial_context="The user wants to learn REST API design"
)

# Continue discovery
response = await skill.respond(
    session_id=session["id"],
    answer="We want it to be scalable and secure"
)

# Generate specification
spec = await skill.generate(
    session_id=session["id"],
    spec_type="specification"  # or "requirements", "architecture"
)
```

### Configuration
```python
from socrates_ai_openclaw import SocraticOpenclawConfig

config = SocraticOpenclawConfig(
    api_key="sk-...",
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=2000,
    knowledge_base_path="/data/kb",
    session_path="/data/sessions"
)
```

## Installation

```bash
# Install from PyPI
pip install socrates-ai-openclaw

# Install with optional dependencies
pip install socrates-ai-openclaw[rag]

# Install for development
pip install socrates-ai-openclaw[dev]
```

## Quick Start

### 1. Basic Discovery Session
```python
import asyncio
from socrates_ai_openclaw import SocraticDiscoverySkill

async def main():
    skill = SocraticDiscoverySkill(api_key="sk-...")

    # Start discovery
    session = await skill.start_discovery(
        topic="Python Web Framework",
        initial_context="User wants to learn about web frameworks"
    )
    print(f"Session ID: {session['id']}")
    print(f"First Question: {session['question']}")

    # User provides answer
    response = await skill.respond(
        session_id=session["id"],
        answer="We're building an API for a mobile app"
    )
    print(f"Next Question: {response['question']}")

    # Generate specification
    spec = await skill.generate(
        session_id=session["id"],
        spec_type="specification"
    )
    print(f"Specification:\n{spec['content']}")

asyncio.run(main())
```

### 2. Resume Existing Session
```python
skill = SocraticDiscoverySkill(api_key="sk-...")

# Load previous session
session = await skill.load_session(session_id="session-123")
print(f"Previous question: {session['question']}")

# Continue from where you left off
response = await skill.respond(
    session_id=session["id"],
    answer="Need to optimize performance"
)
```

### 3. With Knowledge Base
```python
from socrates_ai_openclaw import SocraticDiscoverySkill
from socratic_rag import RAGClient

# Initialize with RAG
rag = RAGClient(provider="chromadb")
await rag.load_documents("/data/docs")

skill = SocraticDiscoverySkill(
    api_key="sk-...",
    rag_client=rag,
    use_rag_context=True
)

# Questions will include relevant context
session = await skill.start_discovery(topic="API Design")
```

## Discovery Session Workflow

### Step 1: Initialize Discovery
```python
session = await skill.start_discovery(
    topic="Your Topic Here",
    initial_context="Optional context about the user"
)

# Returns
{
    "id": "session-123",
    "topic": "Your Topic Here",
    "question": "First Socratic question",
    "created_at": "2026-03-21T10:00:00Z"
}
```

### Step 2: Interactive Questioning
```python
# User provides answer
response = await skill.respond(
    session_id="session-123",
    answer="User's answer to the question"
)

# Returns
{
    "session_id": "session-123",
    "question": "Next Socratic question",
    "context_used": ["doc1.md", "doc2.md"],  # If RAG enabled
    "messages": [...]  # Conversation history
}
```

### Step 3: Continue or Generate
```python
# Continue for more questions
response = await skill.respond(
    session_id="session-123",
    answer="Another answer"
)

# Or generate specification
spec = await skill.generate(
    session_id="session-123",
    spec_type="specification"  # or "requirements", "architecture", "design"
)

# Returns
{
    "session_id": "session-123",
    "type": "specification",
    "content": "Generated specification markdown",
    "generated_at": "2026-03-21T10:05:00Z"
}
```

## Configuration

### Environment Variables
```bash
# Required
export ANTHROPIC_API_KEY="sk-..."

# Optional
export OPENCLAW_MODEL="claude-3-5-sonnet-20241022"
export OPENCLAW_TEMPERATURE="0.7"
export OPENCLAW_MAX_TOKENS="2000"
export OPENCLAW_KNOWLEDGE_BASE="/data/kb"
export OPENCLAW_SESSION_PATH="/data/sessions"
export OPENCLAW_USE_RAG="true"
```

### Programmatic Configuration
```python
from socrates_ai_openclaw import SocraticOpenclawConfig, SocraticDiscoverySkill

config = SocraticOpenclawConfig(
    api_key="sk-...",
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=2000,
    knowledge_base_path="/data/kb",
    session_path="/data/sessions",
    use_rag=True
)

skill = SocraticDiscoverySkill(config=config)
```

## Knowledge Base Integration

### Load Documents
```python
from socratic_rag import RAGClient
from socrates_ai_openclaw import SocraticDiscoverySkill

# Initialize RAG
rag = RAGClient(
    provider="chromadb",
    collection_name="socrates_kb"
)

# Load documents
await rag.load_documents(
    directory="/path/to/documents",
    file_types=[".md", ".txt", ".pdf"]
)

# Create skill with RAG
skill = SocraticDiscoverySkill(
    api_key="sk-...",
    rag_client=rag,
    use_rag_context=True
)
```

### Context-Aware Questions
When RAG is enabled, the skill automatically:
1. Searches knowledge base for relevant documents
2. Includes relevant context in prompts
3. References used documents in responses
4. Adapts questions based on available knowledge

```python
response = await skill.respond(
    session_id="session-123",
    answer="User answer"
)

# Response includes:
print(response["context_used"])  # List of documents used
print(response["context_snippets"])  # Actual content snippets
```

## Session Management

### Session Storage
Sessions are stored as JSON files:

```
/data/sessions/
├── session-123.json
├── session-456.json
└── session-789.json
```

### Session File Format
```json
{
  "id": "session-123",
  "topic": "REST API Design",
  "created_at": "2026-03-21T10:00:00Z",
  "messages": [
    {
      "role": "assistant",
      "content": "What are the main requirements?"
    },
    {
      "role": "user",
      "content": "Scalability and security"
    }
  ],
  "context_used": ["doc1.md"],
  "specifications": []
}
```

### Load and List Sessions
```python
# Load specific session
session = await skill.load_session("session-123")

# List all sessions
sessions = await skill.list_sessions()

# List sessions by topic
sessions = await skill.list_sessions(topic="API Design")

# Get session statistics
stats = await skill.get_session_stats("session-123")
```

## Specification Generation

### Supported Formats
```python
# Generate specification
spec = await skill.generate(
    session_id="session-123",
    spec_type="specification"
)

# Generate requirements
reqs = await skill.generate(
    session_id="session-123",
    spec_type="requirements"
)

# Generate architecture
arch = await skill.generate(
    session_id="session-123",
    spec_type="architecture"
)

# Generate design document
design = await skill.generate(
    session_id="session-123",
    spec_type="design"
)
```

### Custom Templates
```python
# Use custom prompt template
spec = await skill.generate(
    session_id="session-123",
    spec_type="specification",
    custom_prompt="Generate detailed API specification: {messages}"
)
```

### Export Specifications
```python
# Export to markdown
with open("spec.md", "w") as f:
    f.write(spec["content"])

# Export to JSON
import json
with open("spec.json", "w") as f:
    json.dump(spec, f, indent=2)
```

## Event Handling

### Emit Events
```python
from socratic_core import EventEmitter, EventType

skill = SocraticDiscoverySkill(api_key="sk-...")

# Skill emits events automatically:
# - EventType.AGENT_START - When discovery starts
# - EventType.AGENT_COMPLETE - When response generated
# - EventType.AGENT_ERROR - If error occurs

# Listen to events
def on_discovery_start(data):
    print(f"Discovery started: {data['session_id']}")

skill.event_emitter.on(EventType.AGENT_START, on_discovery_start)
```

## Advanced Usage

### Custom Question Generation
```python
class CustomDiscoverySkill(SocraticDiscoverySkill):
    async def generate_next_question(self, session_history):
        """Override question generation"""
        # Custom logic here
        return await super().generate_next_question(session_history)
```

### Batch Processing Sessions
```python
topics = ["API Design", "Database Schema", "Authentication"]

for topic in topics:
    session = await skill.start_discovery(topic=topic)
    response = await skill.respond(
        session_id=session["id"],
        answer="Generic answer"
    )
    spec = await skill.generate(session_id=session["id"])
    print(f"Generated: {topic}")
```

### Error Handling
```python
try:
    session = await skill.start_discovery(topic="Topic")
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Discovery failed: {e}")
```

## Deployment

### As a REST API
```python
from fastapi import FastAPI
from socrates_ai_openclaw import SocraticDiscoverySkill

app = FastAPI()
skill = SocraticDiscoverySkill(api_key="sk-...")

@app.post("/discovery/start")
async def start_discovery(topic: str):
    session = await skill.start_discovery(topic=topic)
    return session

@app.post("/discovery/respond")
async def respond(session_id: str, answer: str):
    response = await skill.respond(session_id=session_id, answer=answer)
    return response

@app.post("/discovery/generate")
async def generate(session_id: str, spec_type: str):
    spec = await skill.generate(session_id=session_id, spec_type=spec_type)
    return spec
```

### With Docker
```dockerfile
FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install -e .

ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

CMD ["python", "-m", "uvicorn", "app:app"]
```

## Testing

```python
import pytest
from socrates_ai_openclaw import SocraticDiscoverySkill

@pytest.fixture
async def skill():
    return SocraticDiscoverySkill(api_key="test-key")

@pytest.mark.asyncio
async def test_start_discovery(skill):
    session = await skill.start_discovery(topic="Test Topic")

    assert session["id"]
    assert session["topic"] == "Test Topic"
    assert session["question"]

@pytest.mark.asyncio
async def test_respond(skill):
    session = await skill.start_discovery(topic="Test")
    response = await skill.respond(
        session_id=session["id"],
        answer="Test answer"
    )

    assert response["question"]
```

## Troubleshooting

### Session Not Found
```python
# Check if session exists
try:
    session = await skill.load_session("session-123")
except FileNotFoundError:
    print("Session not found")
    sessions = await skill.list_sessions()
    print(f"Available sessions: {sessions}")
```

### Knowledge Base Not Loading
```python
# Verify RAG is properly initialized
from socratic_rag import RAGClient

rag = RAGClient(provider="chromadb")
try:
    await rag.load_documents("/path/to/docs")
    print("Documents loaded successfully")
except Exception as e:
    print(f"Failed to load documents: {e}")
```

### API Key Issues
```python
import os

# Check API key is set
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY not set")

# Verify API key works
skill = SocraticDiscoverySkill(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

## Version History

### v0.1.0 (Current)
- Socratic discovery sessions
- Knowledge base integration with ChromaDB
- Specification generation
- Session persistence
- RAG-powered context insertion
- Event system integration

## Contributing

When extending socrates-ai-openclaw:
1. Add tests for new features
2. Update documentation
3. Maintain async patterns
4. Use type hints
5. Emit appropriate events

## Related Documentation

- [Socrates Ecosystem Architecture](../../docs/SOCRATES_ECOSYSTEM_ARCHITECTURE.md)
- [socratic-rag Guide](https://github.com/Nireus79/Socrates/tree/main/docs)
- [socratic-core Guide](https://github.com/Nireus79/Socrates-core/blob/main/docs)

## Support

For issues or questions:
- GitHub Issues: https://github.com/Nireus79/Socrates-ai-openclaw/issues
- Documentation: https://github.com/Nireus79/Socrates-ai-openclaw/tree/main/docs
