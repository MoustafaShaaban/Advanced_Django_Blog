# Advanced Django Blog

A project built with Django web framework and Bootstrap.

###  Project Goals

* All users can read or search for the posts on the blog.

* Authenticated users can:

    * Create, Read, Update and Delete (CRUD) blog posts on the website.

    * Add comments on blog posts, but the comments will not be shown until the website admin approves it.

    * Access their profile which lists all their added blog posts.


### Project preview

* [Youtube](https://www.youtube.com/watch?v=mxe6Ca5yLOo)


###  Project Description:

This project is a Django project called `backend` and it has two registered apps and one third-party app.

    * The `blog` app which contians an app-level templates and urls, used for most of the functionalities of our app, like, models, forms, views, urls, and custom template tags.

    * The `users` app which uses `django.contrib.auth.urls` to allow users register and login to thier accounts.

    * `crispy forms` third-party app which makes beautify django forms design.


### What could you learn from this project?

* Create Django models and define relationships between the database fields.

* Use both Django Class-based and Function-based views.

* Create custom Django template tags, (In this project I created a simple custom template tag that return the number of comments on each blog post).

* How to use page pagination on your website.

* How to associate each blog post to its author.

* How to protect your post so that only you who can modify or delete it.

* Throw a 403 forbidden page to any user who try to guss the URL to change something they are not authorized to do.

* Create a search form on your website.

* And many more.


### Libraries and Packages used

* [Django Web Framework](https://www.djangoproject.com/)

* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) package

* UI components from the official [Bootstrap 5.2](https://getbootstrap.com/docs/5.2/getting-started/introduction/) website documentation.


### To get started with this project

* Clone the repository: git clone https://github.com/MoustafaShaaban/Advanced_Django_Blog.git

* Change directory to backend ``` cd backend ```

* Open the terminal or CMD to create a virtual environment like Python virtual environment (venv) or pipenv and activate it.

    * ``` python -m venv venv ```           *Create the venv*

    * ``` source venv/bin/activate ```      *On Linux*

    * ``` venv/Scripts/activate ```         *On Windows*

    * ``` source venv/Scripts/activate ```  *Git Bash on Windows*

* Install requirements.txt: ``` python -m pip install -r requirements.txt ```

* Change directory to backend ``` cd backend ```

* Create the database by running the following commands:
``` python manage.py makemigrations blog ```
``` python manage.py migrate ```

* Create a super user: ``` python manage.py createsuperuser ```

* Run the project: ``` python manage.py runserver ```

* Open the web browser and go to `http://localhost:8000/` to see the results.