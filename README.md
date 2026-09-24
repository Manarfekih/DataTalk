# DataTalk — Conversational Analytics Agent

DataTalk is a conversational analytics system that turns natural-language business questions into SQL, executes the generated query against PostgreSQL, analyzes the result, and returns a plain-language answer with data suitable for visualization.

The project uses a multi-agent workflow orchestrated with **LangGraph**, combining LLM reasoning, schema exploration, SQL generation, SQL execution, retry handling, SQL memory, relationship-aware schema navigation, safety checks, observability, and evaluation.

---

## ✨ Main Idea

Instead of asking a user to write SQL manually:

```text
"Which customers generated the most orders?"
```

DataTalk follows a workflow similar to:

```text
User Question
     │
     ▼
Question Understanding
     │
     ▼
Schema Exploration
     │
     ▼
SQL Generation
     │
     ▼
SQL Safety Check + Execution
     │
     ├── success ───────────────┐
     │                          ▼
     │                     Result Analysis
     │                          │
     │                          ▼
     │                     Final Answer
     │
     └── failure
            │
            ▼
       SQL Retry / Correction
            │
            └──────────► SQL Execution
```

The workflow is implemented as a graph rather than a single LLM call. This makes each step easier to test, observe, and improve independently.

---

# 🧩 Architecture

## Main components

### 1. Question Understanding Agent

Takes the user's natural-language question and:

- cleans/corrects the user's query,
- identifies the intended request,
- detects when clarification is needed.

### 2. Schema Explorer Agent

Determines which database tables are relevant to the question.

It uses:

- database schema information,
- table relationships,
- the relationship graph.

### 3. Relationship Graph

The database schema is represented as a graph.

Conceptually:

```text
Table ── foreign key ──► Table
```

Tables are nodes and foreign-key relationships are edges.

The graph allows DataTalk to reason about how tables are connected and find relevant paths between tables. Shortest-path search can be useful when the system needs a minimal relationship route between tables.

The relationship graph is used for **schema navigation and relationship reasoning**, not for replacing SQL execution.

### 4. SQL Writer Agent

Generates SQL using:

- the cleaned question,
- relevant tables,
- database schema information.

### 5. SQL Safety

Before execution, generated SQL passes through the project's safety layer.

### 6. SQL Executor

Executes generated SQL against PostgreSQL and records:

- returned rows,
- columns,
- execution result,
- possible errors.

### 7. SQL Retry Agent

When SQL execution fails, the retry path can use:

- the original question,
- failed SQL,
- database error,
- retry history,
- retrieved SQL memories.

It then generates a corrected SQL query and sends it back through execution.

### 8. SQL Memory

DataTalk includes a SQL memory service backed by embeddings and a vector store (chroma).

The purpose is to retrieve semantically similar previous SQL/error situations.

```text
Previous SQL / error
        │
        ▼
   Embedding model
        │
        ▼
 Vector representation
        │
        ▼
    Chroma store
        │
        ▼
Semantic retrieval
        │
        ▼
SQL Retry Agent
```

This is different from the relationship graph:

| Component | Purpose |
|---|---|
| Relationship Graph | Database structure and table relationships |
| Embeddings | Semantic representation of SQL/error experiences |
| Chroma | Vector storage and retrieval |
| SQL Memory | Makes retrieved experiences available to the retry workflow |

### 9. Explanation Agent

After successful execution, the explanation agent receives the question and result data and produces a human-readable answer.

---

# 🧠 Why LangGraph?

LangGraph is used to orchestrate the agentic workflow.

A simple implementation could be:

```text
Question → LLM → SQL → Database → Answer
```

DataTalk instead explicitly represents the workflow and its state:

```text
Question
   ↓
Understand
   ↓
Explore Schema
   ↓
Generate SQL
   ↓
Execute
   ↓
 ┌───────────────┐
 │ Success?      │
 └───────┬───────┘
     Yes │ No
         │
         ▼
    Explanation
         │
         │
         └──────────────► Retry SQL
                              │
                              ▼
                           Execute
```

This makes routing, state management, retries, and observability easier.



---

# 🗂️ Project Structure

```text
DataTalk/
│
├── src/
│   └── datatalk/
│       ├── agents/
│       ├── api/
│       ├── config/
│       ├── database/
│       ├── evaluation/
│       ├── graph/
│       │   ├── nodes.py
│       │   ├── state.py
│       │   └── workflow.py
│       ├── guardrails/
│       ├── llm/
│       ├── memory/
│       ├── models/
│       ├── observability/
│       ├── services/
│       └── utils/
│
├── backend/
├── frontend/
├── data/
├── docs/
├── scripts/
├── tests/
├── logs/
│
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

# 🐘 PostgreSQL Database

DataTalk uses PostgreSQL for the analytics database.

The project uses a Northwind-style relational database for development and evaluation.

The relational structure is important because DataTalk is designed to handle questions requiring relationships between multiple tables.

---

# 🤖 LLM Providers

DataTalk uses an LLM provider abstraction so the application is not tightly coupled to one model implementation.

The provider layer is built around:

```text
BaseLLMProvider
        │
        ├── Gemini provider
        │
        └── other/local providers as configured (qwen)
```

The provider/model is configured through the project's environment/configuration.

---

# 🦙 Ollama Setup

## Important: Ollama is NOT part of this project's Dockerfile

My Ollama container is an **independent shared container**.

It is shared between DataTalk and another project on the same machine.



Architecture:

```text
                 ┌──────────────────┐
                 │   Ollama Server  │
                 │  Docker container│
                 │    port 11434    │
                 └────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             │                         │
        DataTalk                  Other project
```

## Restore Ollama after cloning

If the shared Ollama container does not exist on a new machine, recreate it with:

### Windows CMD

```cmd
docker run -d ^
  --name ollama ^
  -v ollama:/root/.ollama ^
  -p 11434:11434 ^
  --restart unless-stopped ^
  ollama/ollama
```

### Pull the required models

```cmd
docker exec ollama ollama pull qwen3:8b
```

### Verify

```cmd
docker exec ollama ollama list
```

Expected models:

```text

qwen3:8b
```

> The Ollama container is intentionally independent from the DataTalk Docker configuration.

---

# 🔐 Environment Configuration

Create the required local environment configuration.

Do **not** commit:

- API keys
- tokens
- passwords
- private credentials

Typical configuration includes variables such as:

```text
LLM_PROVIDER
GEMINI_MODEL
GEMINI_API_KEY
DATABASE_URL
```

Use the exact variables expected by the current project configuration.

Never publish a real API key on GitHub.

---

# 🐳 Docker

Docker is used for infrastructure such as PostgreSQL.

The important distinction is:

```text
DataTalk Docker infrastructure
        │
        └── PostgreSQL

Independent shared infrastructure
        │
        └── Ollama
```

Ollama is deliberately outside the project's Dockerfile/Compose setup because it is shared by multiple projects.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd DataTalk
```

## 2. Create the Python environment

Use the Python version required by the current `pyproject.toml`.

Example:

```powershell
python -m venv .venv
```

Activate on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Install the project

```powershell
pip install -e .
```

Install any additional development dependencies defined by `pyproject.toml` if required.

## 4. Start PostgreSQL

Start the project's PostgreSQL Docker service using the repository's Docker configuration.

Verify that the database is running before starting the backend.

## 5. Configure environment variables

Create your local environment file and provide the required database and LLM configuration.

## 6. Restore Ollama if needed

Only do this if the shared Ollama container is not already running.

Follow the Ollama Setup section above.

---

# ▶️ Running the Application

The project contains a backend/API and a frontend.

Start the backend using the project's configured entry point.

Then start the frontend separately if you want the user interface.

The API exposes the conversational query functionality through the backend.

If you encounter:

```text
404 Client Error: Not Found
```

for:

```text
http://127.0.0.1:8000/query
```

verify that:

1. the backend is running,
2. the API route exists in the current version,
3. the frontend uses the correct API path,
4. the backend is running on the expected port.

---

# 🔄 Agent Workflow

```text
                    ┌─────────────────────┐
                    │ User Natural Query  │
                    └──────────┬──────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │ Question Understanding │
                  └──────────┬─────────────┘
                             │
                             ▼
                  ┌────────────────────────┐
                  │   Schema Exploration   │
                  │  + Relationship Graph  │
                  └──────────┬─────────────┘
                             │
                             ▼
                  ┌────────────────────────┐
                  │     SQL Generation     │
                  └──────────┬─────────────┘
                             │
                             ▼
                  ┌────────────────────────┐
                  │    SQL Safety Layer    │
                  └──────────┬─────────────┘
                             │
                             ▼
                  ┌────────────────────────┐
                  │     SQL Execution      │
                  └──────────┬─────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                  Error             Success
                    │                 │
                    ▼                 ▼
             ┌──────────────┐  ┌──────────────┐
             │ SQL Retry    │  │ Explanation  │
             │ + SQL Memory │  │    Agent     │
             └──────┬───────┘  └──────┬───────┘
                    │                 │
                    └──► Execute      ▼
                         again      Final Answer
```

---

# 📊 Observability

DataTalk includes tracing and logging to understand what happens during execution.

Typical trace spans include:

```text
question_understanding
schema_exploration
sql_generation
sql_execution
sql_retry
explanation
```

Observability helps answer:

- Which agent ran?
- How long did each step take?
- Where did an error occur?
- Which SQL was generated?
- How did the workflow progress?

Observability is primarily about **runtime behavior**.

---

# 📈 Evaluation

Evaluation is separate from observability.

### Observability asks:

> What happened during the run?

### Evaluation asks:

**Note** : A short evaluation report is included in the repository for a detailed overview of the evaluation methodology, metrics, and results.

> How well did the system perform against a benchmark?

The current benchmark contains **45 questions**.

## Current results

| Metric | Result |
|---|---:|
| Questions | **45** |
| Text-to-SQL accuracy | **8.89%** |
| Execution accuracy | **53.33%** |
| First-pass accuracy | **53.33%** |
| Error rate | **2.3%** |
| Retry success rate | **0%** |
| Average retry count | **0** |

### Text-to-SQL Accuracy — 8.89%

This is a strict SQL exact-match metric.

Only queries matching the reference SQL according to the evaluation criterion are counted as correct.

Different SQL formulations can produce the same result while failing exact string comparison , based on this we can interpret the founded result (8.89%).

In this run:

```text
4 / 45 = 8.89%
```

### Execution Accuracy — 53.33%

This measures whether generated SQL produced the expected database result.

In this evaluation:

```text
24 / 45 = 53.33%
```

This is a more practical metric for a Text-to-SQL application because the final result matters more than reproducing one exact SQL formulation.

### First-Pass Accuracy — 53.33%

This measures questions answered correctly without requiring a retry.

It equals execution accuracy in this run because no retry attempts were recorded.

### Error Rate — 2.3%

The reported error rate is approximately:

```text
1 / 45 ≈ 2.22%
```

which rounds to approximately **2.3%**.

Error rate should be interpreted separately from answer accuracy: a query may execute successfully but still return an incorrect result.

### Retry Success Rate — 0%

No successful retry recoveries were recorded during the 45-question evaluation run because the benchmark did not trigger any retry attempts (average_retry_count = 0).

However, this does not mean that the SQL retry and embedding-based memory system is not working.

The retry mechanism was tested separately using Pytest, where the SQL memory successfully retrieved a relevant previous example from the embedding-based vector store. This confirms that the embedding retrieval component and SQL memory retrieval are functioning correctly.

Therefore:

0% retry success rate reflects the behavior of this particular evaluation dataset, not a failure of the retry or embedding-retrieval implementation.
---

# 🧪 Evaluation vs Observability

```text
OBSERVABILITY
    │
    ├── traces
    ├── latency
    ├── SQL executions
    ├── errors
    └── runtime behavior

EVALUATION
    │
    ├── Text-to-SQL accuracy
    ├── execution accuracy
    ├── first-pass accuracy
    ├── error rate
    └── retry behavior
```

Observability tells you **what happened**.

Evaluation tells you **how well it worked against a benchmark**.

---

# 🧪 Running Evaluation

The evaluation script is located under:

```text
scripts/
```

Run:

```powershell
python scripts/run_evaluation.py
```

For a clean evaluation run, clear previous runtime logs first if they contain cumulative traces/executions:

```powershell
Remove-Item logs\traces.json, logs\executions.json -ErrorAction SilentlyContinue
```

Then:

```powershell
python scripts/run_evaluation.py
```

This helps separate the current evaluation from previous backend/evaluation activity.

---

# 🛡️ SQL Safety

Generated SQL passes through the project's SQL safety layer before database execution.

This is important because SQL is generated dynamically by an LLM.

---

# 🔍 Testing

Tests are located under:

```text
tests/
```

The project uses the testing tooling configured in `pyproject.toml`.

Run the available test suite according to the repository configuration.

---

# 📋 Current Evaluation Snapshot

The current 45-question evaluation is a snapshot of the system.

The results show:

- exact SQL matching is strict,
- practical execution correctness is higher than exact SQL matching,
- more than half of the benchmark questions produced the expected result on the first pass,
- the recorded execution error rate was approximately 2.3%,
- the retry workflow was not triggered in this particular run.

These results provide a baseline for future improvements.

---

# 🛠️ Main Technologies

- **Python**
- **LangGraph**
- **LangChain ecosystem**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic / Pydantic Settings**
- **Gemini / configurable LLM provider**
- **Ollama**
- **Chroma**
- **Embeddings**
- **Plotly**
- **Pandas**
- **Docker**
- **Pytest**

---


# 👤 Project Goal

DataTalk was designed as a practical AI and data engineering project rather than a simple chatbot.

It combines:

```text
LLMs
+
Multi-agent workflow
+
LangGraph orchestration
+
Relational databases
+
Schema reasoning
+
Relationship graph
+
Text-to-SQL
+
SQL safety
+
SQL execution
+
Error recovery
+
Semantic SQL memory
+
Vector search
+
Observability
+
Evaluation
```

The goal is to make database analytics accessible through natural language while keeping the system modular, observable, and testable.

---

# 📌 Development Notes

The project separates:

- agents,
- graph orchestration,
- database services,
- LLM providers,
- memory,
- guardrails,
- observability,
- evaluation.

This allows individual components to be improved independently.

For example:

```text
Change LLM provider
        ↓
LLM provider layer

Improve SQL correction
        ↓
SQL Retry Agent

Improve schema navigation
        ↓
Relationship Graph / Schema Explorer

Improve benchmark
        ↓
Evaluation scripts
```

---

## Author

**Manar El Fakih Romdhane**

Data Science Engineering Student  
AI / Machine Learning / Data Engineering

GitHub: https://github.com/Manarfekih
