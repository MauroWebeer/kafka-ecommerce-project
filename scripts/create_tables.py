import psycopg2
from psycopg2 import sql
import os

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Connect to PostgreSQL (connect to the default "postgres" database first)
conn = psycopg2.connect(
    dbname="postgres", user=db_user, password=db_password, host=db_host
)
conn.autocommit = True  # Make sure changes are committed automatically
cur = conn.cursor()

# Create database if it doesn't exist
def create_database():
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ecommerce';")
    exists = cur.fetchone()
    if not exists:
        cur.execute("CREATE DATABASE ecommerce;")
        print("Database 'ecommerce' created successfully!")
    else:
        print("Database 'ecommerce' already exists.")

# Connect to the new database
def connect_to_ecommerce_db():
    conn.close()
    return psycopg2.connect(
        dbname="ecommerce", user=db_user, password=db_password, host=db_host
    )

# Create tables
def create_tables():
    # Connect to the ecommerce database
    conn = connect_to_ecommerce_db()
    cur = conn.cursor()

    # Step 1: Create tables WITHOUT foreign keys
    create_users_table = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''

    create_events_table = '''
    CREATE TABLE IF NOT EXISTS events (
        event_id UUID PRIMARY KEY,
        event_name VARCHAR(255),
        event_type VARCHAR(50),
        created_at TIMESTAMP
    );
    '''

    create_transactions_table = '''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id UUID PRIMARY KEY,
        user_id INT,
        transaction_amount DECIMAL(10, 2),
        timestamp TIMESTAMP,
        event_id UUID -- This is just an identifier, NOT a foreign key anymore
    );
    '''

    create_page_views_table = '''
    CREATE TABLE IF NOT EXISTS page_views (
        page_view_id UUID PRIMARY KEY,
        user_id INT,
        path VARCHAR(255),
        timestamp TIMESTAMP,
        event_id UUID
    );
    '''

    create_clicks_table = '''
    CREATE TABLE IF NOT EXISTS clicks (
        click_id UUID PRIMARY KEY,
        user_id INT,
        path VARCHAR(255),
        timestamp TIMESTAMP,
        event_id UUID
    );
    '''

    # Execute table creation
    cur.execute(create_users_table)
    cur.execute(create_events_table)
    cur.execute(create_transactions_table)
    cur.execute(create_page_views_table)
    cur.execute(create_clicks_table)

    # Step 2: Add foreign key constraints separately
    add_constraints = [
        '''
        ALTER TABLE transactions 
        ADD CONSTRAINT fk_transactions_user FOREIGN KEY (user_id) REFERENCES users(user_id),
        ADD CONSTRAINT fk_transactions_event FOREIGN KEY (event_id) REFERENCES events(event_id);
        ''',
        '''
        ALTER TABLE page_views 
        ADD CONSTRAINT fk_page_views_user FOREIGN KEY (user_id) REFERENCES users(user_id),
        ADD CONSTRAINT fk_page_views_event FOREIGN KEY (event_id) REFERENCES events(event_id);
        ''',
        '''
        ALTER TABLE clicks 
        ADD CONSTRAINT fk_clicks_user FOREIGN KEY (user_id) REFERENCES users(user_id),
        ADD CONSTRAINT fk_clicks_event FOREIGN KEY (event_id) REFERENCES events(event_id);
        '''
    ]

    for constraint in add_constraints:
        try:
            cur.execute(constraint)
        except psycopg2.errors.DuplicateObject:
            print("Foreign key constraint already exists, skipping...")

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully!")

if __name__ == "__main__":
    # Step 1: Create database
    create_database()

    # Step 2: Create tables
    create_tables()
