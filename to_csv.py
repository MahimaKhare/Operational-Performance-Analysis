import psycopg2

# Connection
conn = psycopg2.connect(
    dbname="inventory",
    user="postgres",
    password="Rpsingh123",
    host="localhost",
    port="5432"
)

tables = [
    "vendor_sales_summary"
]

for table in tables:
    filename = f"{table}.csv"
    with open(filename, "w", encoding="utf-8") as f:
        cursor = conn.cursor()
        cursor.copy_expert(f"COPY {table} TO STDOUT WITH CSV HEADER", f)
    print(f"✅ Exported {table} to {filename}")
    
conn.close()