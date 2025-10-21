#!/usr/bin/env python3
from app.routes import app

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port=5000)

    #  to use gunicorn app:app, create app/__init__.py like this:
    app.run()