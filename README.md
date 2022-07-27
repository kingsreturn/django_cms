# WebFramework_WenfengYang

Git Repository zur Diplomarbeit Webbasiertes Cloudframework für CM

-- Download the project and run the following command

make sure uacpp server is installed and running and the mysql server user and database is created

# Setup on Windows
```shell
cd .\webframework_wenfengyang\django_cms
virtualenv -p python3 venv
.\venv\Scripts\activate.bat
pip install -r requirements_origin.txt
```
# Setup on Linux
```bash
cd .\webframework_wenfengyang\django_cms
virtualenv -p python3 venv
source venv/bin/activate
pip install -U -r requirements_origin.txt
```
# Run it:

```bash
cd site1/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The webpage will be showed on http://localhost:8000
