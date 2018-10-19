# Setting up
- Create database.secret.sh file with the correct credentials

# Run Development Server
- Activate credentials (source database.secret.env)
- Create venv, install requirements & run script ('FLASK_APP=app.py flask run' or 'env FLASK_APP=app.py flask run')

# Run Docker
- Build Docker
- Run docker (docker run -p 5000:5000 ...)
