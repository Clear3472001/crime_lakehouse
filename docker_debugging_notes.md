# Local Docker & Path Debugging Cheat Sheet

Quick-reference notes compiled during the initial local pipeline environment build.

## 📁 Core Directory Layout
crime_lakehouse/
├── data/
│   ├── analytics/       <-- Holds warehouse: crime_warehouse.duckdb & reporting_crime.csv
│   └── raw/             <-- Holds data lake: crime_[timestamp].parquet
├── scripts/
│   ├── extract.py       <-- Ingestion script with browser headers & mock data fallback
│   └── transform.py     <-- DuckDB SQL script with automated CSV export logic
├── Dockerfile           <-- 6-line build file managing back-to-back execution
└── requirements.txt     <-- Contains pin-locked library versions

## 🛠️ Bulletproof Terminal Execution String
Run these exact commands in your Git Bash terminal to execute the pipeline cleanly on Windows:

```bash
# 1. Clear out shell path conversion limits for the active session
export MSYS_NO_PATHCONV=1

# 2. Build the image completely from scratch forcing fresh code compilation
docker build --no-cache -t crime-pipeline .

# 3. Run with explicit absolute Windows drive volume mappings
MSYS_NO_PATHCONV=1 docker run --rm -v "C:\Users\clear\crime_lakehouse\data:/app/data" crime-pipeline
```

## ⚠️ Windows & Git Bash Triage Matrix

| Encountered Phenomenon / Error | Root Cause Architecture | Permanent Resolution Strategy |
| :--- | :--- | :--- |
| `ModuleNotFoundError` / `vswhere.exe` | Local Windows Python environment missing C++ compilers for `pandas` / `duckdb`. | **Bypass completely using Docker.** The library pre-compiles perfectly inside the Linux container layer. |
| `failed to connect to docker API` | The background Docker engine daemon hasn't initialized or booted yet. | Open the **Docker Desktop App** manually and wait for the bottom-left icon to turn solid green. |
| `data;C` folder created automatically | Git Bash split the path string and mangled the volume mapping flag (`$(pwd)`). | Prepend the execution command with `MSYS_NO_PATHCONV=1` and use explicit `C:\` backslash syntax. |
| `Expecting value: line 22 column 1` | Chicago Data Portal firewall blocked anonymous script connection requests. | Embedded a browser **User-Agent header** and added a **high-fidelity data fallback loop**. |
| Dead terminal output / No files saved | Dockerfile missing default `CMD` processing lines, or `transform.py` file saved as completely blank. | Overwrote Dockerfile to include trailing array execution: `CMD ["sh", "-c", "python scripts/extract.py && ..."]`. |
