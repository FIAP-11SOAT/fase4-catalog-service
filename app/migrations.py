"""
Database migration runner
Executes SQL migrations automatically on application startup
"""
import os
from pathlib import Path
from sqlalchemy import text
from .db import engine
import logging

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).parent.parent / "migrations"


def run_migrations():
    """
    Run all SQL migration files in order
    This is executed on application startup
    """
    try:
        logger.info("🚀 Starting database migrations...")
        
        if not MIGRATIONS_DIR.exists():
            logger.warning(f"⚠️  Migrations directory not found: {MIGRATIONS_DIR}")
            return
        
        # Get all SQL files sorted by name
        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
        
        if not migration_files:
            logger.info("📝 No migration files found")
            return
        
        # Execute each migration file
        with engine.connect() as conn:
            for migration_file in migration_files:
                logger.info(f"📄 Running migration: {migration_file.name}")
                
                with open(migration_file, 'r', encoding='utf-8') as f:
                    migration_sql = f.read()
                
                try:
                    # Execute the migration SQL
                    # Use text() for raw SQL execution
                    conn.execute(text(migration_sql))
                    conn.commit()
                    logger.info(f"✅ Migration {migration_file.name} completed successfully")
                    
                except Exception as e:
                    error_msg = str(e).lower()
                    # Ignore errors for things that already exist
                    if any(keyword in error_msg for keyword in [
                        'already exists',
                        'duplicate key',
                        'unique constraint',
                        'violates unique constraint'
                    ]):
                        logger.info(f"⚠️  Migration {migration_file.name} - objects already exist (skipping)")
                        conn.rollback()
                    else:
                        logger.error(f"❌ Migration {migration_file.name} failed: {e}")
                        conn.rollback()
                        raise
        
        logger.info("✅ All migrations completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Migration error: {e}")
        # Don't crash the application if migrations fail
        # This allows the app to start even if migrations have issues
        logger.warning("⚠️  Application starting despite migration errors")
