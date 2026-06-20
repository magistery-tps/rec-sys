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
