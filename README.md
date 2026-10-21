# Containerized Public Safety Data Lakehouse Pipeline

A production-grade, local data engineering pipeline that extracts public safety data from a REST API, establishes an immutable columnar file-based Data Lake (Bronze Layer), and executes transactional SQL transformations inside an embedded data warehouse (Gold Layer) utilizing **Python**, **SQL**, **DuckDB**, and **Docker**.

## 🔗 Live Analytics Dashboard
👉 [Click here to view the live interactive Looker Studio Dashboard](https://datastudio.google.com/reporting/79e7aacd-db17-4ecc-9d98-322b808de409)

## 📊 Pipeline Architecture & Data Flow

1. **Ingestion Layer (Python):** Connects to the Chicago Data Portal API using custom request headers to handle perimeter firewalls, featuring an automated data fallback mechanism to maintain pipeline continuity.
2. **Storage Layer (Data Lake / Bronze):** Converts raw API payloads directly into compressed Apache Parquet format to optimize disk I/O and preserve native data types.
3. **Warehouse Layer (DuckDB / Gold):** Automatically initialises a persistent DuckDB database engine, reads the columnar lake files directly, and builds analytical summary tables using relational ANSI SQL.
4. **DevOps Layer (Docker):** Containers the runtime dependencies, isolating the entire process to prevent local environment drift or operating system path conflicts.

---

## 🏆 Data Engineering Achievements & Skills Demonstrated

### 🔹 Advanced Ingestion & Resilience
* **Network Emulation:** Configured specialized User-Agent request structures to safely interface with external data portal infrastructure.
* **Pipeline Guardrails:** Implemented a robust data fallback strategy that hooks connection errors, writing high-fidelity mock assets to the storage drive to ensure subsequent database states never enter a broken configuration.

### 🔹 Architectural Modeling & Warehousing
* **Columnar Lakehouse Storage:** Designed a local physical Data Lake utilizing Snappy-compressed Parquet files, mirroring true modern enterprise data architectures (Delta Lake/Iceberg).
* **Embedded Analytics Engine:** Configured an in-process serverless DuckDB data warehouse layer to execute high-speed, local analytics without the cost or overhead of heavy cloud computing blocks.
* **Relational SQL Transformations:** Authored sequential SQL scripts handling explicit data type castings, table schemas, and multi-attribute aggregations (`GROUP BY`, `ORDER BY`).

### 🔹 Containerization & DevOps Mastery
* **Multi-Stage Orchestration:** Engineered a single, extensionless configuration `Dockerfile` managing the complete pipelined execution sequence (`extract.py && transform.py`) back-to-back.
* **Local Drive Volume Mounting:** Configured Docker runtime container mounts (`-v`) to cleanly bridge isolated Linux files systems with local host Windows drives, guaranteeing persistent storage on the physical disk.
* **Cross-Platform Path Standardization:** Successfully ironed out shell path translations (`MSYS_NO_PATHCONV`) and OneDrive virtualization sync conflicts by designing local path abstractions.

---

## 🛠️ The Core Technical Stack

| Capability | Technology / Paradigm |
| :--- | :--- |
| **Orchestration / Language** | Python 3.11-slim |
| **Packaging & Containers** | Docker Engine & Buildx |
| **Virtualization Engine** | Windows Subsystem for Linux (WSL 2) |
| **Data Lake Storage Layer** | Apache Parquet (Snappy Compressed) |
| **Data Warehousing Engine** | DuckDB Core Storage |
| **Transformation Logic** | Advanced Relational ANSI SQL |

---

## 🚀 Local Deployment & Verification Steps

To reproduce this pipeline environment locally, clone the repository and run the following execution string inside your Git Bash terminal:

```bash
# 1. Package the pipeline dependencies and scripts into an immutable image
docker build -t crime-pipeline .

# 2. Run the pipeline end-to-end with a local C-Drive folder volume mount
MSYS_NO_PATHCONV=1 docker run --rm -v "C:\Users\clear\crime_lakehouse\data:/app/data" crime-pipeline
```
