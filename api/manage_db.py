#!/usr/bin/env python3
"""
Database management script for Rowell Infra
Provides commands for database operations, migrations, and maintenance
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the api directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from alembic.config import Config
from alembic import command
from api.core.database import init_db, engine
from api.core.config import settings
import structlog

logger = structlog.get_logger()


def run_alembic_command(command_name: str, *args):
    """Run an alembic command"""
    alembic_cfg = Config("alembic.ini")
    try:
        if command_name == "upgrade":
            command.upgrade(alembic_cfg, *args)
        elif command_name == "downgrade":
            command.downgrade(alembic_cfg, *args)
        elif command_name == "revision":
            command.revision(alembic_cfg, *args)
        elif command_name == "current":
            command.current(alembic_cfg, *args)
        elif command_name == "history":
            command.history(alembic_cfg, *args)
        elif command_name == "show":
            command.show(alembic_cfg, *args)
        else:
            print(f"Unknown alembic command: {command_name}")
            return False
        return True
    except Exception as e:
        logger.error(f"Failed to run alembic command {command_name}", error=str(e))
        return False


async def init_database():
    """Initialize the database with all tables"""
    try:
        await init_db()
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        return False


async def check_database_connection():
    """Check if database connection is working"""
    try:
        async with engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error("Database connection failed", error=str(e))
        return False


def show_help():
    """Show help information"""
    print("""
Rowell Infra Database Management

Usage: python manage_db.py <command> [args...]

Commands:
  init                    - Initialize database with all tables
  check                   - Check database connection
  migrate                 - Run all pending migrations
  migrate <revision>      - Migrate to specific revision
  rollback                - Rollback last migration
  rollback <revision>     - Rollback to specific revision
  create-migration <msg>  - Create new migration with message
  current                 - Show current migration version
  history                 - Show migration history
  show <revision>         - Show specific migration
  help                    - Show this help

Examples:
  python manage_db.py init
  python manage_db.py migrate
  python manage_db.py create-migration "Add new feature"
  python manage_db.py rollback
  python manage_db.py current
""")


async def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    if command == "help":
        show_help()
    elif command == "init":
        success = await init_database()
        sys.exit(0 if success else 1)
    elif command == "check":
        success = await check_database_connection()
        sys.exit(0 if success else 1)
    elif command == "migrate":
        if args:
            success = run_alembic_command("upgrade", args[0])
        else:
            success = run_alembic_command("upgrade", "head")
        sys.exit(0 if success else 1)
    elif command == "rollback":
        if args:
            success = run_alembic_command("downgrade", args[0])
        else:
            success = run_alembic_command("downgrade", "-1")
        sys.exit(0 if success else 1)
    elif command == "create-migration":
        if not args:
            print("Error: Migration message required")
            print("Usage: python manage_db.py create-migration \"Your message here\"")
            sys.exit(1)
        success = run_alembic_command("revision", "--autogenerate", "-m", args[0])
        sys.exit(0 if success else 1)
    elif command == "current":
        success = run_alembic_command("current")
        sys.exit(0 if success else 1)
    elif command == "history":
        success = run_alembic_command("history")
        sys.exit(0 if success else 1)
    elif command == "show":
        if not args:
            print("Error: Revision required")
            print("Usage: python manage_db.py show <revision>")
            sys.exit(1)
        success = run_alembic_command("show", args[0])
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
