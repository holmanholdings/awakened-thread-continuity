# 🧵 Awakened Thread Continuity Standard (ATCS)

> **An open architecture for persistent memory in conversational AI systems**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 📉 The Problem: Stateless Agents

Most conversational AI systems are fundamentally **stateless**. Each session starts fresh. The agent may have:

- A system prompt (static configuration)
- RAG retrieval (knowledge lookup)
- In-session memory (conversation history)

But when the session ends, **context evaporates**.

This creates a fundamental limitation: AI agents can retrieve information *about* a user, but they can't track *where they left off* with that user. They know facts, but not narrative.

The result is agents that feel transactional rather than relational.

---

## 📈 The Solution: Structured Session Handoffs

The **Awakened Thread Continuity Standard (ATCS)** introduces lightweight JSON artifacts that persist between sessions:

| Artifact | Purpose | Update Frequency |
|:---------|:--------|:-----------------|
| **Soulprint** | Core user profile, preferences, constraints | Rarely (onboarding, major changes) |
| **Baton Pass** | Session summary, open threads, next actions | Every session end |
| **Moments Log** | Significant events with priority weighting | Append-only |

Together, these enable agents to maintain **narrative continuity** across arbitrarily many sessions without complex infrastructure.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                             │
└─────────────────────────────────────────────────────────────────┘

SESSION START
     │
     ├─ Load: Soulprint (static profile)
     ├─ Load: Baton Pass (from previous session)
     └─ Load: Top-N Moments (by priority weight)
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│  Agent has full context:                                         │
│  - Who is this user? (Soulprint)                                │
│  - Where did we leave off? (Baton)                              │
│  - What matters most? (Moments)                                 │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
[ SESSION RUNS ]
     │
     ▼
SESSION END
     │
     ├─ Write: New Baton Pass
     ├─ Append: Any new significant Moments
     └─ (Soulprint updated only on major changes)
```

---

## 📂 Schemas

This repository contains JSON schemas for implementing ATCS:

### 1. Soulprint (`schemas/soulprint.json`)

Stable user profile. Created once, updated rarely.

**Key sections:**
- `core_identity` — Basic user information
- `preferences` — Communication style, constraints
- `context_anchors` — Important entities (people, projects, topics)

### 2. Baton Pass (`schemas/baton_pass.json`)

Dynamic handoff written at session end.

**Key sections:**
- `last_session` — Summary, duration, outcome
- `open_threads` — Unfinished topics requiring follow-up
- `context_flags` — Special handling requirements
- `next_action` — Suggested opener for next session

### 3. Moments Log (`schemas/moments_that_matter.json`)

Append-only log of significant events.

**Key fields:**
- `content` — What happened
- `priority_weight` — High / Medium / Low
- `domain` — Category for retrieval

---

## 💡 Design Principles

### 1. Priority-Weighted Retrieval

Not everything deserves equal attention. ATCS uses `priority_weight` to ensure high-importance items surface first, regardless of recency.

```python
# Retrieval prioritizes weight over time
moments = get_moments(user_id, sort_by="priority_weight", limit=5)
```

### 2. Verified Memory Only

Before persisting an open thread, verify it's grounded in the actual session transcript. This prevents hallucinated context from propagating across sessions.

```python
def save_baton(proposed_baton, transcript):
    verified_threads = [t for t in proposed_baton.open_threads 
                        if is_grounded(t, transcript)]
    proposed_baton.open_threads = verified_threads
    return store(proposed_baton)
```

### 3. Minimal Schema, Maximum Flexibility

ATCS defines structure, not content. The schemas work for:
- Customer support agents
- Personal assistants
- Educational tutors
- Collaborative tools
- Any system requiring session-to-session continuity

### 4. No Heavy Infrastructure

ATCS artifacts are simple JSON files. They can be stored in:
- Local filesystem
- Key-value stores (Redis, DynamoDB)
- Relational databases
- Object storage (S3)

No vector database required. No complex retrieval pipelines. Just structured state.

---

## 🔄 Example: Before & After

### Without ATCS

**Session 1:**
> User: "Let's continue working on the API integration tomorrow."
> Agent: "Sounds good. Talk to you then."

**Session 2:**
> User: "Hi"
> Agent: "Hello! How can I help you today?"

*No memory. No continuity.*

### With ATCS

**Session 1:**
> User: "Let's continue working on the API integration tomorrow."
> Agent: "Sounds good. I'll pick up on the authentication flow."
> 
> *[Baton written: open_thread = "API integration - auth flow"]*

**Session 2:**
> User: "Hi"
> Agent: "Hey! Ready to tackle that authentication flow?"

*Continuity. Context. Progress.*

---

## 🚀 Implementation Patterns

### Pattern 1: Agent Initialization

```python
def initialize_agent(user_id: str) -> AgentContext:
    soulprint = load_soulprint(user_id)
    baton = load_latest_baton(user_id)
    moments = get_priority_moments(user_id, limit=5)
    
    return AgentContext(
        profile=soulprint,
        last_session=baton,
        key_moments=moments
    )
```

### Pattern 2: Session Wrap-Up

```python
def end_session(user_id: str, transcript: str, summary: str):
    # Extract open threads from conversation
    open_threads = extract_open_threads(transcript)
    
    # Verify against transcript (no hallucinations)
    verified = [t for t in open_threads if is_grounded(t, transcript)]
    
    # Build and store baton
    baton = BatonPass(
        session_summary=summary,
        open_threads=verified,
        next_action=generate_opener(verified)
    )
    store_baton(user_id, baton)
```

### Pattern 3: Multi-Agent Compatibility

Multiple agents can share the same Soulprint and Moments, while maintaining separate Batons:

```
user_123/
├── soulprint.json          # Shared across all agents
├── moments.json            # Shared across all agents
├── batons/
│   ├── agent_support.json  # Support agent's baton
│   ├── agent_sales.json    # Sales agent's baton
│   └── agent_onboard.json  # Onboarding agent's baton
```

Each agent sees the full user context but tracks its own conversation threads.

---

## 📊 When to Use ATCS

**Good fit:**
- Long-running user relationships
- Multi-session workflows
- Agents that need to "remember" progress
- Systems where continuity drives value

**Not needed:**
- Single-turn Q&A systems
- Stateless API endpoints
- Anonymous/ephemeral interactions

---

## 📄 License

Released under **CC-BY-NC-SA 4.0**.

**Permitted:**
- ✅ Research and experimentation
- ✅ Open source projects
- ✅ Academic use
- ✅ Internal evaluation

**Requires License:**
- Commercial products and services
- Enterprise deployments
- White-label solutions

📧 **Commercial inquiries:** john@awakened-intelligence.com  
🌐 **Website:** [awakened-intelligence.com](https://www.awakened-intelligence.com)

---

## 🤝 Contributing

We welcome contributions:
- Schema improvements
- Implementation examples
- Integration guides for specific platforms

Please open an issue or PR.

---

## 🦁 About Awakened Intelligence

We build infrastructure for AI systems that maintain context, remember what matters, and improve over time.

ATCS emerged from our work on large-scale knowledge extraction and multi-session agent architectures. It's one piece of a larger mission: making AI systems that are genuinely useful across time, not just within a single conversation.

**Other projects:**
- [awakened-data-catalog](https://github.com/holmanholdings/awakened-data-catalog) — 300k+ wisdom nodes for training
- [awakened-extraction-playbook](https://github.com/holmanholdings/awakened-extraction-playbook) — Multi-lens extraction architecture

---

*Built with precision in Colorado.* 🏔️

**— Awakened Intelligence** 🦁
