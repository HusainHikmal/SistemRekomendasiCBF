# tests/conftest.py
import sys
import os
import sqlite3
import pandas as pd
import pytest

# Ensure project root is on sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import config
from models import create_db
from seed_data import insert_data


@pytest.fixture(scope='session', autouse=True)
def setup_test_database(tmp_path_factory):
    """
    Creates a temporary SQLite database, initializes schema and seeds data.
    This runs once per test session automatically.
    """
    # Create a temporary file for the database
    db_file = tmp_path_factory.mktemp('data') / 'test_smartphones.db'
    # Override the DATABASE_PATH
    config.Config.DATABASE_PATH = str(db_file)
    # Initialize schema and seed data
    create_db()
    insert_data()


@pytest.fixture
def client():
    """
    Provides a Flask test client with TESTING=True
    """
    from app import app
    app.config['TESTING'] = True
    return app.test_client()
