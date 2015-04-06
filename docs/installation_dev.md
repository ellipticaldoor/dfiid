# Create a virtualenv for the dfiid project

```
mkirtualenv --python=[your_python_3_path] dfiid
```

You can find your python3 path with:

```
which python3
```


# Add postactivate and predeactivate files to the virtualenv 

```
vim ~/.virtualenvs/dfiid/bin/postactivate
vim ~/.virtualenvs/dfiid/bin/predeactivate
```

You can find an example of this files in the docs folder on the root of the repo.
Remember to fill it with your on configuration.


# On /dfiif/project/ folder

```
workon dfiid
pip install -r requirements/base.txt
python manage.py makemigrations user user_profile sub content
python manage.py migrate
python manage.py syncdb
python manage.py runserver
```