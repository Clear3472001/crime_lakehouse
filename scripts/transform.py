import os
import duckdb

def run_transformations():
    print("🔄 Starting DuckDB Transformations...")
    
    # Establish persistent database file connection
    os.makedirs("data/analytics", exist_ok=True)
    db_path = "data/analytics/crime_warehouse.duckdb"
    conn = duckdb.connect(db_path)
    
    # 1. Create a Silver/Staging Table from raw files using DuckDB's auto-inference
    print("Creating staging layer from raw files...")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS staging_crime AS 
        SELECT * FROM 'data/raw/crime_*.parquet'
    """)
    
    # 2. Build a Clean Gold/Analytics Production Table with proper SQL types
    print("Building analytical dimensional tables...")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analytic_daily_crime_summary (
            summary_date DATE,
            primary_type VARCHAR,
            arrest_made BOOLEAN,
            total_incidents INT
        )
    """)
    
    # 3. Perform an incremental Upsert (Merge) to aggregate incidents safely
    conn.execute("""
        INSERT INTO analytic_daily_crime_summary
        SELECT 
            CAST(date AS DATE) as summary_date,
            primary_type,
            CAST(arrest AS BOOLEAN) as arrest_made,
            COUNT(*) as total_incidents
        FROM staging_crime
        GROUP BY 1, 2, 3
    """)
    
    # Quick data quality verification output
    sample = conn.execute("""
        SELECT primary_type, SUM(total_incidents) as total 
        FROM analytic_daily_crime_summary 
        GROUP BY 1 
        ORDER BY total DESC 
        LIMIT 3
    """).fetchall()
    
    print("📊 Top 3 Crime Categories Sample:", sample)
        # 4. Export the clean production table to a CSV for BI tools
    print("📋 Exporting optimized visualization layer to CSV...")
    conn.execute("""
        COPY analytic_daily_crime_summary 
        TO 'data/analytics/reporting_crime.csv' 
        (HEADER, DELIMITER ',');
    """)
    conn.close()
    print("✅ Transformations complete and saved to disk.")

if __name__ == "__main__":
    run_transformations()