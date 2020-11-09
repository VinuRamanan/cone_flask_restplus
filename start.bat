pip install -r requirements.txt
python create_db_tables.py
if not exist "C:\yarn_application\" mkdir C:\yarn_application
copy settings.json c:\yarn_application\settings.json
python service.py install