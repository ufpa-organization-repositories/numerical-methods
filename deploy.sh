# install heroku cli
sudo snap install --classic heroku

# nano Procfile
# web: gunicorn app:app

# nano .python-version
# 3.8.8

# nano runtime.txt
# python-3.8.8

# installing requirements
source venv-numerical-methods/bin/activate
pip install -r requirements.txt

# create requirements.txt
pip freeze > requirements.txt