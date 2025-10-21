from .routes import app

# to use gunicorn app:app, create app/__init__.py 
# Make the app available when importing the app package
__all__ = ['app']

