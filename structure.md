# Module 1 — Introduction

This module teaches the **core building blocks of LangGraph workflows**.

Think of LangGraph as **a graph of AI steps**:

```
User Input
   ↓
LLM
   ↓
Tool
   ↓
Decision
   ↓
Output
```

---

## Lesson 1: Motivation

**Why LangGraph exists.**

Problem with normal LLM apps:

```
Prompt → LLM → Output
```

Problems:

* No control
* No looping
* Hard to add tools
* Hard to debug
* No state management

LangGraph solves this by creating **structured AI workflows**.

Example:

```
User question
   ↓
Planner
   ↓
Tool
   ↓
Evaluation
   ↓
Answer
```

---

## Lesson 2: Simple Graph

A **graph** is a workflow made of:

```
Nodes → Edges → State
```

Example:

```
START → Chatbot → END
```

Code idea:

```python
workflow.add_node("chatbot", chatbot)
workflow.set_entry_point("chatbot")
workflow.add_edge("chatbot", END)
```

Each **node = function**.

---

## Lesson 3: LangSmith Studio

Uses **LangSmith**.

LangSmith helps with:

* Debugging agents
* Observing agent runs
* Viewing graph execution
* Inspecting messages

Example trace:

```
User
 ↓
Agent
 ↓
Tool
 ↓
Agent
 ↓
Final answer
```

This is critical for **production AI systems**.

---

## Lesson 4: Chain

A **chain** is the simplest workflow.

Example:

```
Prompt → LLM → Output
```

LangGraph version:

```
START → LLM → END
```

Code idea:

```python
workflow.add_node("llm", call_llm)
```

Chains are **linear workflows**.

---

## Lesson 5: Router

A **router decides which path to take**.

Example:

User question types:

```
Math question → Calculator tool
Weather question → Weather API
General question → LLM
```

Graph example:

```
User
 ↓
Router
 ↙     ↘
Math   Weather
 ↓       ↓
Answer  Answer
```

Router logic:

```python
def route(state):
    if "weather" in question:
        return "weather_node"
```

---

## Lesson 6: Agent

An **agent decides which tool to use**.

Example workflow:

```
User Question
     ↓
Agent (LLM reasoning)
     ↓
Tool call
     ↓
Agent again
     ↓
Final answer
```

Example:

```
User: What is 25 * 32?

Agent → calculator tool
Agent → answer
```

This is **ReAct architecture**.

---

## Lesson 7: Agent with Memory

Adds **conversation memory**.

Without memory:

```
User: My name is Sam
User: What is my name?
```

LLM forgets.

With memory:

```
State.messages
```

Example state:

```python
class State(TypedDict):
    messages: list
```

Messages accumulate.

---

## Lesson 8: Intro to Deployment (Optional)

Deploy your agent.

Example platforms:

* API server
* cloud services
* production agent platform

Typical deployment:

```
Frontend
   ↓
API
   ↓
LangGraph agent
   ↓
LLM + tools
```

---

# Module 2 — State and Memory

This module explains **how LangGraph stores information between steps**.

State is the **heart of LangGraph**.

---

## Lesson 1: State Schema

Define what your agent remembers.

Example:

```python
class AgentState(TypedDict):
    messages: list
    user_query: str
```

State travels through every node.

```
Node → modify state → next node
```

---

## Lesson 2: State Reducers

Reducers control **how state updates**.

Example:

Appending messages:

```
Old messages + new messages
```

Reducer example:

```python
messages: Annotated[list, add_messages]
```

This ensures messages **merge correctly**.

---

## Lesson 3: Multiple Schemas

Different parts of graph use **different state structures**.

Example:

```
Research agent state
Chatbot state
Memory state
```

This helps manage **complex workflows**.

---

## Lesson 4: Trim and Filter Messages

Problem:

Conversation gets too long.

Example:

```
100+ messages
```

LLMs have token limits.

Solution:

* trim messages
* filter irrelevant messages
* keep important context

Example:

```
Keep last 5 messages
```

---

## Lesson 5: Chatbot with Summarizing Memory

Instead of storing everything:

Old messages → summarized.

Example:

```
Conversation history
↓
Summary
↓
Stored memory
```

This keeps context small.

---

## Lesson 6: Chatbot with External Memory

Store memory **outside the graph**.

Example storage:

* vector database
* database
* knowledge store

Workflow:

```
User
 ↓
Retrieve memory
 ↓
Agent
 ↓
Response
```

---

# Module 3 — UX and Human-in-the-Loop

This module improves **user experience and control**.

---

## Lesson 1: Streaming

Instead of waiting for full response:

User sees:

```
Typing...
```

Example streaming:

```
Hello
How
can
I
help?
```

Streaming improves UX.

---

## Lesson 2: Breakpoints

Pause graph execution.

Example:

```
User question
 ↓
Agent decision
 ↓
BREAKPOINT
 ↓
Human review
 ↓
Continue
```

Useful for:

* auditing
* debugging
* human approval

---

## Lesson 3: Editing State

Humans can modify state.

Example:

```
Agent extracted wrong data
Human edits it
Agent continues
```

---

## Lesson 4: Dynamic Breakpoints

Breakpoints triggered automatically.

Example:

```
If tool confidence < threshold
→ pause
```

This adds safety.

---

## Lesson 5: Time Travel

You can **rewind the agent execution**.

Example:

```
Step 1
Step 2
Step 3
```

Go back to step 2 and rerun.

Used for debugging.

---

# Module 4 — Building Your Assistant

This module teaches **advanced workflow architectures**.

---

## Lesson 1: Parallelization

Run nodes **simultaneously**.

Example:

```
User query
   ↓
Search web
Search database
Search documents
   ↓
Combine results
```

This speeds up agents.

---

## Lesson 2: Sub-graphs

Large workflows broken into smaller graphs.

Example:

```
Main assistant
   ↓
Research graph
   ↓
Analysis graph
```

This improves modularity.

---

## Lesson 3: Map-Reduce

Used for **large datasets**.

Example:

```
100 documents
```

Map phase:

```
Summarize each document
```

Reduce phase:

```
Combine summaries
```

Used in:

* document analysis
* research assistants

---

## Lesson 4: Research Assistant

Example project:

```
User question
 ↓
Search internet
 ↓
Read sources
 ↓
Summarize
 ↓
Generate report
```

This is a **multi-agent research system**.

---

# Module 5 — Long-Term Memory

This module teaches **persistent memory**.

---

## Lesson 1: Short vs Long-Term Memory

Short-term memory:

```
Conversation context
```

Long-term memory:

```
User preferences
Knowledge
History
```

Example:

```
User likes Python
User works in finance
```

---

## Lesson 2: LangGraph Store

LangGraph provides a **memory storage system**.

Stores:

* conversation data
* user data
* agent knowledge

---

## Lesson 3: Memory Schema + Profile

Define memory structure.

Example:

```
User profile
Name
Preferences
Skills
```

---

## Lesson 4: Memory Schema + Collection

Store multiple memories.

Example:

```
Research notes
Documents
User conversations
```

Stored as collections.

---

## Lesson 5: Agent with Long-Term Memory

Full system:

```
User
 ↓
Retrieve memory
 ↓
Agent reasoning
 ↓
Update memory
 ↓
Response
```

Example:

```
User: I love Python
Agent stores preference
```

---

# Module 6 — Deployment

This module shows **how to run agents in production**.

---

## Lesson 1: Deployment Concepts

Production system architecture:

```
Frontend
 ↓
API
 ↓
LangGraph agent
 ↓
LLM
 ↓
Tools
```

---

## Lesson 2: Creating a Deployment

Steps:

1. Build graph
2. Package app
3. Deploy server
4. Connect LLM

---

## Lesson 3: Connecting to Deployment

Clients connect via:

```
API
SDK
Frontend
```

Example:

```
Web UI
Slack bot
Mobile app
```

---

## Lesson 4: Double Texting

Problem:

User sends **multiple messages quickly**.

Example:

```
User: Hello
User: Actually wait
User: New question
```

Agent must handle **concurrent messages safely**.

---

## Lesson 5: Assistants

Create reusable assistants.

Example assistants:

```
Customer support bot
Research assistant
Coding assistant
Data analysis agent
```

---

# After This Course You Will Know

You will understand how to build:

```
Chatbots
AI Agents
Research agents
RAG systems
Multi-agent systems
AI assistants
```

using **LangGraph.

---
