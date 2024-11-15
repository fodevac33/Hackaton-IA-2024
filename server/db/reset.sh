rm hackaton.db

echo "Applying migrations..."

sqlite3 hackaton.db < migrations/001_create_tables.sql
sqlite3 hackaton.db < migrations/002_insert_sample_data.sql

echo "Database has been reset."