@echo off
REM setup_postgres.bat - Script d'installation PostgreSQL Windows

echo 🚀 Urban Flow - Configuration PostgreSQL
echo ========================================

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé
    echo 📦 Veuillez installer Python 3.9+ depuis https://python.org
    pause
    exit /b 1
)

REM Créer environnement virtuel
echo 🔧 Création de l'environnement virtuel...
python -m venv venv
call venv\Scripts\activate.bat

REM Installer les dépendances
echo 📦 Installation des dépendances Python...
pip install -r requirements.txt

REM Vérifier si PostgreSQL est installé
echo 🔍 Vérification de PostgreSQL...
where psql >nul 2>&1
if errorlevel 1 (
    echo ❌ PostgreSQL n'est pas installé
    echo.
    echo 📦 Veuillez installer PostgreSQL:
    echo 1. Télécharger depuis https://www.postgresql.org/download/windows/
    echo 2. Installer avec les options par défaut
    echo 3. Ajouter PostgreSQL au PATH
    echo.
    echo 🔧 Configuration recommandée:
    echo   - Port: 5432
    echo   - Mot de passe superuser: postgres
    echo   - Base de données: postgres
    echo.
    echo ⚠️  Redémarrez le script après installation
    pause
    exit /b 1
)

REM Tester la connexion
echo 🧪 Test de connexion PostgreSQL...
psql -U postgres -c "SELECT version();" >nul 2>&1
if errorlevel 1 (
    echo ❌ Impossible de se connecter à PostgreSQL
    echo ℹ️  Essayez avec: psql -U postgres
    echo.
    echo 🔧 Assurez-vous que:
    echo   - PostgreSQL est démarré
    echo   - Le mot de passe est correct
    echo   - Le service PostgreSQL est en cours d'exécution
    pause
    exit /b 1
)

REM Initialiser la base de données
echo ⚙️  Initialisation de la base de données...
python init_postgresql.py

echo.
echo 🎉 Configuration PostgreSQL terminée !
echo 👉 Lancez l'application avec: python src\app.py
pause