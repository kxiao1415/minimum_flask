# minimum_flask

1. install and start redis:
$brew install redis
$redis-server

2. install requirements:
$pip install -r requirements.txt

3. create log and file storage folders
$ mkdir ../minimum_flask_log
$ touch ../minimum_flask_log/flask_backend.log
$ mkdir ../minimum_flask_storage

4. start flask
python run.py