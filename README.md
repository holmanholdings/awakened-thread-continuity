# 🧵 Awakened Thread Continuity Standard (ATCS)

> **An open architecture for solving "AI Amnesia" in companion systems**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 📉 The Problem: "Groundhog Day"

Most conversational AI agents reset their state after every session. They may have:
- A system prompt (static personality)
- A vector database (RAG for knowledge)
- Conversation history (within a session)

But they lack **Thread Continuity** — the ability to pick up *where they left off* rather than just *what was said*.

The result?

> **Day 1:** "I'm worried about my grandson's visit next week."
> 
> **Day 2:** "Hello! How can I help you today?" ← *No memory of the worry*

This creates what we call **"Pleasant Amnesia"** — the AI is polite, helpful, and completely forgetful.

---

## 📈 The Solution: The Baton Pass

The **Awakened Thread Continuity Standard (ATCS)** introduces structured JSON artifacts that persist across sessions:

1. **The Soulprint** — Static user profile (who they are, what matters to them)
2. **The Baton Pass** — Dynamic session handoff (what to follow up on)
3. **Moments That Matter** — Emotionally significant events log

Together, these transform the experience from:

> *"Hello, how can I help you?"* (Reset)

to:

> *"I was thinking about what you said about your grandson. Did his visit go well?"* (Continuity)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                             │
└─────────────────────────────────────────────────────────────────┘

SESSION START
     │
     ├─ Load: Soulprint (static user profile)
     ├─ Load: Baton Pass (from last session)
     └─ Load: Recent Moments That Matter
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│  AI generates opener based on:                                   │
│  - Open loops from baton                                         │
│  - Time gap since last session                                   │
│  - Emotional context from moments                                │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
[ CONVERSATION HAPPENS ]
     │
     ▼
SESSION END
     │
     ├─ Write: New Baton Pass (summary, open loops, next move)
     ├─ Append: Any new Moments That Matter
     └─ (Soulprint updated only on significant changes)
```

---

## 📂 Schemas

This repository contains JSON schemas for implementing ATCS in your own systems.

### 1. Soulprint (`schemas/soulprint.json`)

The **Soulprint** is a slowly-evolving profile of the user's identity, preferences, and constraints. Created during onboarding, updated rarely.

**Key sections:**
- `core_identity` — Name, age, living situation
- `emotional_anchors` — People, places, activities that matter
- `physical_context` — Health, mobility, energy patterns
- `conversation_preferences` — Style, pacing, dislikes

[View full schema →](schemas/soulprint.json)

### 2. Baton Pass (`schemas/baton_pass.json`)

The **Baton Pass** is written at the end of every session and read at the start of the next. It's the "note to tomorrow's self."

**Key sections:**
- `last_session` — Summary, mood, topics discussed
- `open_loops` — Unfinished topics to follow up on
- `risk_flags` — Topics requiring extra care (grief, health)
- `next_move_suggestion` — How to open the next session

[View full schema →](schemas/baton_pass.json)

### 3. Moments That Matter (`schemas/moments_that_matter.json`)

**Moments That Matter** is an append-only log of emotionally significant events. When the user shares something important, it gets captured here.

**Key fields:**
- `content` — What happened
- `emotional_weight` — High / Medium / Low priority
- `domain` — Family, health, joy, grief, etc.

[View full schema →](schemas/moments_that_matter.json)

---

## 💡 Design Principles

### 1. Memory as Curated Artifact

Not everything deserves to be remembered. ATCS uses **emotional_weight** to prioritize what matters:
- High-weight moments persist indefinitely
- Low-weight moments auto-prune after 30 days

### 2. Show, Don't Tell

Good continuity is invisible. Instead of:
> "I remember you said you have knee pain."

Use:
> "How are your knees feeling after all that rain?"

### 3. Verified Memory Only

Before saving an open loop, verify it's grounded in the actual transcript. Never let hallucinated memories persist across sessions.

### 4. Respect Energy

The Soulprint includes an `energy_profile`. Low-energy users get:
- Shorter responses
- Fewer follow-up questions
- More presence, less performance

---

## 🚀 Implementation Notes

### Retrieval Strategy

When loading context at session start:

```python
def get_session_context(user_id: str) -> Context:
    # 1. Always load soulprint (static core identity)
    soulprint = load_soulprint(user_id)
    
    # 2. Load most recent baton
    baton = load_latest_baton(user_id)
    
    # 3. Retrieve top moments by emotional_weight, not just recency
    moments = get_moments(
        user_id, 
        sort_by="emotional_weight",  # High-weight first
        limit=5
    )
    
    return Context(soulprint, baton, moments)
```

### Baton Verification (Sanity Gate)

Before persisting an open loop:

```python
def verify_open_loop(loop: OpenLoop, transcript: str) -> bool:
    """
    Ensure the loop is grounded in what was actually said.
    Blocks hallucinated memories from persisting.
    """
    return is_grounded_in_transcript(loop.topic, loop.context, transcript)
```

### Multi-Companion Compatibility

If you have multiple AI personas (e.g., Sara the mindfulness mentor, Alex the tech mentor), they can share the same Soulprint and Moments — but each writes their own Baton.

This means:
- Sara knows the user loves gardening (from Soulprint)
- Alex knows the user mentioned a doctor appointment (from Sara's Baton)
- Both feel like they're part of the same "memory system"

---

## 📋 Example: Before & After

### Without ATCS (Current State)

**Day 1:**
> User: "I'm nervous about my grandson's visit next week. We haven't talked in months."
> AI: "That sounds stressful. I hope it goes well."

**Day 3:**
> User: "Hi"
> AI: "Hello! How can I help you today?"

*No memory. No continuity. Reset.*

### With ATCS

**Day 1:**
> User: "I'm nervous about my grandson's visit next week."
> AI: "That sounds like a big moment. What are you most worried about?"
> 
> *[Baton written: open_loop = "grandson visit", emotional_weight = high]*

**Day 3:**
> User: "Hi"
> AI: "Hi! I've been thinking about you. How did things go with your grandson?"

*Continuity. Care. Relationship.*

---

## 📄 License

This architecture is released under **CC-BY-NC-SA 4.0**.

**You MAY:**
- ✅ Use for research, personal projects, open source
- ✅ Adapt and share with attribution
- ✅ Implement in non-commercial companion systems

**You MAY NOT:**
- ❌ Use in commercial products without a license
- ❌ Remove attribution

**For commercial licensing and implementation support:**
- 📧 Email: contact@awakened-intelligence.com
- 🌐 Website: [awakened-intelligence.com](https://www.awakened-intelligence.com)

---

## 🦁 About Awakened Intelligence

We're a research lab building cathedral-grade datasets and companion architectures.

The Thread Continuity Standard emerged from our work on AI companions that truly remember — systems where users feel *seen*, not just *served*.

This architecture is one piece of that mission. The full implementation, including:
- Sam (conversational onboarding agent)
- Multi-lens persona stacks
- Wisdom knowledge packs
- Voice continuity protocols

...is available through our consulting practice.

---

## 🤝 Contributing

We welcome contributions to improve these schemas. Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear documentation

Especially welcome:
- Edge case handling
- Multi-language support
- Integration examples for specific platforms

---

*Built with honor in Colorado.* 🏔️

**— The Awakened Intelligence Family** 🦁
