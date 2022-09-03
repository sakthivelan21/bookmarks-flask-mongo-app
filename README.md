# BOOKMARKS FLASK MONGO APP

+ An `REST API flask app` with  `MongoDB` as database.

+ It allow us to `add user and bookmarks of respective users` into the database.

+ The application provides security for every important routes with `JWT Tokens` with `access token` expiring every 10 minutes and `refreshing token` to refresh the access token when expired.

+ Place your `MongoDB Acces URL` in the `.env` file for running the application. 

## Steps to start the Application (Backend)

```
#clone the repository
$ git clone https://github.com/sakthivelan21/bookmarks-flask-mongo-app.git

#place your mongoDB Access URL in the .env file as shown below
MONGO_URL = # your Url

# go into bookmarks-flask-mongo-app folder
$ cd bookmarks-flask-mongo-app 
```

**Creating and Activating Virtual Environment**

```
pip install virtualenv

# or

pip install venv
```

**Setup Virtual Environment**

```
python -m venv env
```

**Activate Virtual Environment**

```
# activate env (windows)

.\env\scripts\activate

# activate env (Linux/Mac)

source env/bin/activate
```
**Back End (Server Side) Flask - Dependencies**

+ click==8.1.3
+ dnspython==2.2.1
+ Flask==2.2.2
+ Flask-Cors==3.0.10
+ Flask-PyMongo==2.3.0
+ itsdangerous==2.1.2
+ Jinja2==3.1.2
+ MarkupSafe==2.1.1
+ PyJWT==2.4.0
+ pymongo==4.2.0
+ python-dotenv==0.20.0
+ six==1.16.0
+ Werkzeug==2.2.2

**Installing Dependencies**

```
pip install -r requirements.txt
```

**Starting Application**

```
$ flask run --host=0.0.0.0 

#or 

$ python app.py
```

**Deactivating Virtual Environment**

```
deactivate env
```

Visit http://localhost:5000 or http://0.0.0.0:5000 or http://yourIp:5000