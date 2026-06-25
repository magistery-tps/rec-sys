# OpenCode Guidelines for Recommendation System (rec-sys)

## Context & Project Overview
- **Documentation**: The `README.md` file in this directory contains highly relevant and detailed information about the project. Please refer to it for deeper context.
- **Domain**: End-to-End Recommendation System (Collaborative Filtering, Content-Based, Embeddings).
- **Environment**: Conda/Mamba environment `recsys` (Python 3.11). See `environment.yml` for full dependencies (Django, PyTorch, Surprise, Sentence-Transformers, MySQL).

## Project Structure & Navigation
- **`recsys/`**: The core Django project and application. 
  - `recsys/recsys/`: Django settings and core routing.
  - `recsys/recsysweb/`: The main Django app containing Web Views, Models, Templates, and the REST API endpoints (`urls.py`).
- **`src/`**: Shared Domain/Worker codebase. This directory contains scripts, jobs, and services that perform heavy Machine Learning tasks (like computing distance matrices). It interacts with the Django application via a REST Client (`api.RecSysApi`) initialized in `domain_context.py`.
- **`dags/`**: Apache Airflow DAGs.
  - ⚠️ **CRITICAL RULE**: The files in `dags/` are the **source of truth**. Do NOT modify DAGs in `~/airflow`. Always modify them here in `~/rec-sys/dags/`.
- **`bin/`**: Python scripts called by the Airflow DAGs to execute specific jobs.
- **`notebooks/`**: Exploratory data analysis (EDA) and experimental ML code.

## REST API Endpoints
The Django application exposes the following REST API under the `/api/` base path (served by Django REST Framework routers and custom views):
- **Core Entities (CRUD ViewSets):**
  - `/api/users/`
  - `/api/items/`
  - `/api/interactions/`
  - `/api/recommenders/`
- **Matrices Data:**
  - `/api/similarity-matrix/`
  - `/api/similarity-matrix-cells/`
- **Recommendation / Inference Views:**
  - `GET /api/recommender/<recommender_id>/users/<user_id>/items` (Predicts top items for a specific user)
  - `GET /api/recommender/<recommender_id>/users/<user_id>/items/<item_id>/similar` (Finds similar items to a specific item based on a chosen recommender model)

## Airflow DAGs
The system relies on Airflow to run heavy matrix computations asynchronously. The definitions are in the `dags/` folder:
- **`1_bert_item_distance_matrix_dag.py`**: Computes item distance matrices using the BERT model `all-MiniLM-L12-v2`.
- **`2_bert_item_distance_matrix_dag.py`**: Computes item distance matrices using the BERT model `all-MiniLM-L6-v2`.
- **`3_bert_item_distance_matrix_dag.py`**: Computes item distance matrices using the BERT model `all-mpnet-base-v2`.
- **`4_bert_item_distance_matrix_dag.py`**: Computes item distance matrices using the BERT model `multi-qa-mpnet-base-dot-v1`.
- **`nfm_distance_matrix_dag.py`**: Computes user-item or item-item similarity matrices using the **NMF** (Non-Negative Matrix Factorization) model.
- **`svd_distance_matrix_dag.py`**: Computes similarity matrices using the **SVD** (Singular Value Decomposition) collaborative filtering model.

## Architecture & Data Flow
1. **Web Interface & API**: The Django application (`recsysweb`) manages user accounts, UI rendering, and exposes the REST API serving users, items, interactions, and computed matrices.
2. **Background Jobs (Airflow)**: DAGs trigger scripts in `bin/` on a scheduled interval (e.g. `*/3 * * * *`).
3. **ML Worker Logic (`src/`)**: These scripts load the `DomainContext`, pull data from the Django API, run Machine Learning algorithms (PyTorch, Surprise, SVD, BERT) to compute similarities, and push the resulting matrices back to the Django API to be served to end users.

## Global Conventions
- **Database**: Django uses MySQL/MariaDB. Schema changes must be done via Django Migrations (`manage.py makemigrations`).
- **Separation of Concerns**: Django (`recsys/`) should only handle HTTP routing, database modeling, and serving responses. Heavy machine learning and data crunching belongs in `src/` or `notebooks/`.


## Extra instructions
### Agent development cycle (default, unless overridden)
#### Mandatory Workflow Enforcement (Tool Usage)
- **You MUST use the `todowrite` tool** at the very beginning of every new feature, bugfix, or refactor request.
- You are strictly forbidden from writing production code before populating your TODO list with the following exact 5-step lifecycle:
  1. **Analyze & Plan:** Analyze the requirement and propose a plan to the user. STOP and wait for approval.
  2. **TDD (RED):** Write failing unit/integration tests that specify the desired behavior.
  3. **TDD (GREEN):** Implement the minimum production code necessary to pass the tests.
  4. **Refactor & Quality Gate:** Refactor the code applying SOLID principles, Clean Code, and explicitly handling errors/exceptions.
  5. **Final Verification:** Run all quality checks (`pytest`, linters).
- Keep the `todowrite` status updated in real-time as you progress through each step. Never skip the RED phase.
- **Plan once:** Before coding, propose a TODO list oriented to iterative implementation and STOP. Ask for approval once. After approval, proceed without asking for the plan again unless new information invalidates it.
- **Test-first (when supported):** If the repo has an existing test framework, write/update tests that specify the new behavior before implementing the production change.
- **Quality gate (must answer "yes" before finishing):**
    - **Task alignment:** Does the change meet every requirement from the original request (and nothing unrelated)?
    - **Tests for new logic:** Did I add/adjust unit tests covering the success path and relevant error or edge cases?
    - **Idiomatic + consistent:** Does the implementation follow Python and repo conventions?
    - **Clarity + simplicity:** Is the code easy to read and minimizes complexity?
    - **Error handling:** Are failure modes handled explicitly, with no silent failures?
- **Final verification:** Run the applicable validation commands (e.g., `pytest`).

### Architecture instructions

#### General Software Design & OOP Principles

**1. The SOLID Principles**
* **Single Responsibility (SRP):** A class should have one, and only one, reason to change. Keep components strictly focused.
* **Open/Closed (OCP):** Software entities should be open for extension but closed for modification.
* **Liskov Substitution (LSP):** Subclasses must be substitutable for their base classes without breaking the application.
* **Interface Segregation (ISP):** Prefer multiple, highly specific interfaces over a single, general-purpose one.
* **Dependency Inversion (DIP):** High-level modules should not depend on low-level modules; both should depend on abstractions. Depend on interfaces, not on concrete implementations.

**2. DRY (Don't Repeat Yourself)**
* Avoid duplicating code or logic. Every piece of knowledge must have a single, unambiguous representation.

**3. KISS (Keep It Simple, Stupid)**
* Systems work best when they are kept simple rather than made complicated.

**4. YAGNI (You Aren't Gonna Need It)**
* Always implement things when you actually need them, never when you just foresee that you might need them in the future.

**5. Law of Demeter (Principle of Least Knowledge)**
* An object should assume as little as possible about the structure of other objects. It should only interact with its immediate dependencies.

**6. High Cohesion**
* Ensure that all the methods and properties within a class are strongly related and focused on a unified purpose.

**7. Low Coupling**
* Minimize the dependencies between different classes. Changes in one class should have little to no impact on other classes.

#### Python Object-Oriented Programming (OOP) Best Practices

**1. Type Hinting Strictness**
* Always use type hints (`typing` module, or built-in generic types) for function signatures, arguments, and class attributes.

**2. Leverage Dataclasses and Pydantic**
* Use `@dataclass` or Pydantic `BaseModel` for classes whose primary purpose is to hold data. This significantly reduces boilerplate and provides built-in validation.

**3. Strict Encapsulation**
* Hide implementation details. Use single leading underscores `_` to indicate internal/private methods and instance variables. Expose only what is necessary through public methods or properties.

**4. Avoid Mutable Default Arguments**
* Never use mutable structures (like `[]` or `{}`) as default arguments in functions to prevent unexpected side effects across function calls.

**5. Composition over Inheritance**
* Avoid inheriting from concrete classes whenever possible. If you need to extend behavior, prefer composition and dependency injection.

**6. Explicit Exception Handling**
* Catch specific exceptions rather than broad `Exception` classes. Fail fast and explicitly. Never use bare `except:` clauses.

#### Development methodology and code quality

**1. Test-Driven Development (TDD)**
- **Mandatory Approach:** All system changes (new features, bug fixes, refactoring) must be designed and implemented using **Test-Driven Development (TDD)**.
- **Red-Green-Refactor Cycle:**
  1. **Red:** Write a unit or integration test that fails, specifying the desired behavior.
  2. **Green:** Implement the minimum code necessary to make the test pass successfully.
  3. **Refactor:** Clean and optimize the implemented code, ensuring it follows the style guidelines and application architecture without breaking the tests.

**2. Mutation Testing**
- **Test Suite Validation:** To ensure the quality and actual effectiveness of the tests, apply **Mutation Testing** principles.
- **Goal:** Validate that the test suite is robust and fails in the presence of mutations. If tests still pass after changing logic, they are not rigorously validating the expected behavior.
