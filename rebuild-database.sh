rm db.sqlite3

python3 ./manage.py migrate

python3 ./manage.py loaddata users
python3 ./manage.py loaddata tokens
python3 ./manage.py loaddata user_types
python3 ./manage.py loaddata employees
python3 ./manage.py loaddata tags
python3 ./manage.py loaddata projects
python3 ./manage.py loaddata project_users
python3 ./manage.py loaddata priorities
python3 ./manage.py loaddata bug_statuses
python3 ./manage.py loaddata bug_types
python3 ./manage.py loaddata bugs 
python3 ./manage.py loaddata comments
python3 ./manage.py loaddata bug_tags
python3 ./manage.py loaddata bug_projects