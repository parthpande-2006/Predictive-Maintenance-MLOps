import sqlite3
import os
import pandas as pd

DB_PATH = 'data/telementry_storage.db'
def initialize_database():
    os.makedirs('data', exist_ok =True)
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machine_metadata (
            machine_id INTEGER PRIMARY KEY,
            product_serial TEXT NOT NULL,
            machine_type TEXT NOT NULL
        );
    """)
    raw_df = pd.read_csv('data/ai4i2020.csv')
    metadata_df = raw_df[['UDI', 'Product ID', 'Type']].copy()
    metadata_df.columns = ['machine_id', 'product_serial','machine_type']
    metadata_df.to_sql('machine_metadata', connection, if_exists='replace', index=False)
    cursor.execute('SELECT COUNT(*) FROM machine_metadata;')
    total_rows = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    print(f'SQL Database Seeding Complete. {total_rows} machine profiles mapped successfully')

if __name__ == '__main__':
    initialize_database()
                        

                         
