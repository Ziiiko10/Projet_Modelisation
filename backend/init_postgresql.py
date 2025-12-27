"""
Script d'initialisation PostgreSQL pour Urban Flow
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

def create_database():
    """Create database and user for Urban Flow"""
    
    # Get configuration from environment
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_admin_user = os.getenv('POSTGRES_ADMIN_USER', 'postgres')
    db_admin_password = os.getenv('POSTGRES_ADMIN_PASSWORD', 'postgres')
    
    db_name = os.getenv('POSTGRES_DB', 'urbanflow_db')
    db_user = os.getenv('POSTGRES_USER', 'urbanflow')
    db_password = os.getenv('POSTGRES_PASSWORD', 'urbanflow123')
    
    print("🚀 Initialisation de PostgreSQL pour Urban Flow")
    print(f"📊 Base de données: {db_name}")
    print(f"👤 Utilisateur: {db_user}")
    
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_admin_user,
            password=db_admin_password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"📦 Création de la base de données: {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print("✅ Base de données créée")
        else:
            print("ℹ️  Base de données existe déjà")
        
        # Close connection to create new one to the database
        cursor.close()
        conn.close()
        
        # Connect to the new database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_admin_user,
            password=db_admin_password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (db_user,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"👤 Création de l'utilisateur: {db_user}")
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'")
            print("✅ Utilisateur créé")
        
        # Grant privileges
        print("🔑 Attribution des privilèges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")
        cursor.execute(f"ALTER USER {db_user} WITH SUPERUSER")
        
        # Create extensions if needed
        print("🔧 Création des extensions...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
        
        cursor.close()
        conn.close()
        
        print("🎉 Initialisation PostgreSQL terminée avec succès!")
        print("\n📋 Configuration pour .env:")
        print(f"DATABASE_URL=postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        
        # Test connection
        test_connection(db_host, db_port, db_name, db_user, db_password)
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        sys.exit(1)

def test_connection(host, port, database, user, password):
    """Test database connection"""
    print("\n🧪 Test de connexion...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connecté à PostgreSQL: {version[0]}")
        
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        print(f"📊 Base de données: {db_name[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Échec de connexion: {e}")

def create_env_file():
    """Create .env file with PostgreSQL configuration"""
    env_content = """# Flask Configuration
FLASK_ENV=development
SECRET_KEY=dev-secret-key-urbanflow-2024
DEBUG=true

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_ADMIN_USER=postgres
POSTGRES_ADMIN_PASSWORD=postgres
POSTGRES_DB=urbanflow_db
POSTGRES_USER=urbanflow
POSTGRES_PASSWORD=urbanflow123

# Database URL (auto-generated)
DATABASE_URL=postgresql://urbanflow:urbanflow123@localhost:5432/urbanflow_db

# Simulation Configuration
MOCK_MODE=true
MOCK_VEHICLE_COUNT=50
MOCK_TRAFFIC_LIGHT_COUNT=5

# WebSocket Configuration
SOCKETIO_ASYNC_MODE=eventlet
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n📄 Fichier .env créé avec configuration PostgreSQL")
    else:
        print("\nℹ️  Fichier .env existe déjà")

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Urban Flow - Initialisation PostgreSQL")
    print("=" * 50)
    
    create_env_file()
    print()
    create_database()