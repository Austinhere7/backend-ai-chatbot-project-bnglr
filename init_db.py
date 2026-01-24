"""
Database initialization script.
Creates tables and enables pgvector extension.
"""
from sqlalchemy import text
from app.config.database import engine, Base
from app.models.models import Session, Message, Document, DocumentChunk


def init_db():
    """
    Initialize the database.
    Creates the pgvector extension and all tables.
    """
    # Create pgvector extension
    with engine.connect() as conn:
        # Enable pgvector extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database initialized successfully!")
    print("Tables created:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")


if __name__ == "__main__":
    init_db()
