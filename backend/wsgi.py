"""
WSGI entry point for production deployment
"""
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app as application

if __name__ == "__main__":
    application.run()