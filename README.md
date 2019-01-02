# django_forum
The implementation is in english but the templates are in portuguese
This is a simple forum based on django framework.

It´s features are:
* email confirmation and activation
* users allowed to post are defined by admin
* all users can comment and respond other comments
* gamitization implementation is on-going. 
* implementation of a set of subjects to post 
* implementation of a set of rules to game
* profile personalization with personal photo

Configuration
* email and password for the server. Tested on google. MUST BE DONE BEFORE RUN THE SERVER


this is not a framework, but a complete project. 
istalation
git clone
cd django-forum
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser 
****give username, email and password to your superuser****
python manage.py runserver

on the browser, go to http://127.0.0.1/8000/admin
and click the profiles option.
Go to the botton of the page and select is_allowed_to_post and is_activated

now go to http://127.0.0.1/8000/

the option to post should apear to you. Log off now and go to the http://127.0.0.1/8000/

Click "Cadastrar usuario" to create a new user.
Your user will not be able to post.

Enjoy!