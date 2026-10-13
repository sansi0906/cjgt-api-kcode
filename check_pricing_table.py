import psycopg2
from config import PG_CONFIG
conn = psycopg2.connect(host=PG_CONFIG['host'], port=PG_CONFIG['port'], database=PG_CONFIG['database'], user=PG_CONFIG['user'], password=PG_CONFIG['password'])
cursor = conn.cursor()

# Get table structure
cursor.execute("""
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'cjgt_service_pricing'
ORDER BY ordinal_position
""")
rows = cursor.fetchall()
print('=== cjgt_service_pricing columns ===')
for row in rows:
    print(f'{row[0]}: {row[1]}, nullable={row[2]}, default={row[3]}')

cursor.close()
conn.close()
