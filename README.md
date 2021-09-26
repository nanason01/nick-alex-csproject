# nick-alex-csproject

Run instructions:

first time:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

after that:
```
source env/bin/activate
```

To create a new db:

```
sqlite3 sql/sqlite_db < sql/schema.sql
```