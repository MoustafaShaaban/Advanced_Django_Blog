# Advanced Django Blog

A blog project built using 

  [Django Web Framework](https://www.djangoproject.com/), 
  [Django REST Framework](https://www.django-rest-framework.org), 
  [Graphene Django](https://docs.graphene-python.org/projects/django/en/latest/), 
  [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django),
  [HTMX](https://htmx.org/),
  [Vue.js 3](https://vuejs.org/),
  [Quasar Framework](https://quasar.dev/),
  [Tanstack Vue Query](https://tanstack.com/query/latest/docs/vue/overview),
  [Vue Apollo](https://apollo.vuejs.org/),
  [Vue-multiselect](https://vue-multiselect.js.org/),


[Full Review](https://moustafashaaban.github.io/project-reviews/django/Django-Blog/Django-Blog/)

###  Project Goals

* Authenticated users can:

  * Access a GraphQL endpoint and run several Quries and CRUD Mutations.

  * Access a Rest API endpoint and run CRUD operations.

  * Create, Read, Update and Delete (CRUD) blog posts on the website.

  * Add comments on blog posts, but the comments will not be visiable until the website admin approves it.

  * Like Blog posts and Add them to their favorite list (using HTMX).

  * Access their profile which lists all their blog posts and their favorite posts.


* All users can read or search for the posts on the blog.

* Users can access separate frontend project built using Vue.js 3, Tanstack-Vue-Query, Vue-Apollo and Quasar Framework which connects with django through Django Rest Framework using Session Authentication.

* The frontend vue.js app also allows users to perform CRUD operations through connecting to a REST API and a GraphQL endpoints.

Currently in Vue frontend users can:

* Register for an account and log in to their account (users will be authenticated using Django Rest Framework Session Authentication).

* Add tags to blog using a Rest API endpoint and GraphQL endpoint.

* Perform CRUD operations to blog posts using both REST API and GraphQL.

* Perform CRUD operations to add comments to blog posts using both REST API and GraphQL.

* Add and remove posts to and form their favorite posts list.

* Access pages that show their added blog posts and their favorite posts.

* Search for blog posts by title and limiting the results using both REST API and GraphQL

### Project preview

* [Youtube](https://www.youtube.com/watch?v=mxe6Ca5yLOo)

* [Article](https://moustafashaaban.github.io/project-reviews/django/Django-Blog/Django-Blog/)


###  Project Description:

This project is a Django project called `blog_backend` and it has four registered apps and one third-party app.

  * The `blog` app which contains an app-level templates and urls, used for most of the functionalities of our app, like, models, forms, views, urls, and custom template tags.

  * The `api` app which contains the Django Rest Framework integration used to build a REST API.

  * The `graphql_app` which contains the Graphene Django integration used to build a GraphQL endpoint.
    
  * The `users` app which uses `django.contrib.auth.urls` to allow users register and login to their accounts.

  * `crispy forms` third-party app which beautify django forms design.


### What could you learn from this project?

* Create Django models and define relationships between the database fields.

* Use both Django Class-based and Function-based views.

* Create custom Django template tags, (In this project I created a simple custom template tag that return the number of comments on each blog post).

* How to use page pagination on your website.

* How to associate each blog post to its author.

* How to protect your post so that only you who can modify or delete it.

* Throw a 403 forbidden page to any user who try to guess the URL to change something they are not authorized to change.

* Create a search form on your website.

* And many more.


### To get started with this project without Docker:

* Make sure that both [PostgreSQL](https://www.postgresql.org/) database and [Mailpit](https://mailpit.axllent.org/) Email client are installed and running in your system.

* Create a PostgreSQL database, This project uses PostgreSQL version 14.

* Export database default url using the following terminal command, In this example PostgreSQL is installed locally, database name is django-blog-backend, and database admin credentials are => username: admin / password: 1234:

```bash
export DATABASE_URL=postgres://admin:1234@127.0.0.1:5432/django-blog-backend
```

* Open the terminal or CMD to create a virtual environment like Python virtual environment (venv) or pipenv and activate it.

    * ``` python -m venv venv ```           *Create the venv*

    * ``` source venv/bin/activate ```      *On Linux*

    * ``` venv/Scripts/activate ```         *On Windows*

    * ``` source venv/Scripts/activate ```  *Git Bash on Windows*

* Change directory to django_blog_backend ``` cd django_blog_backend ```

* Install local.txt requirements file: ``` python -m pip install -r requirements/local.txt ```

* Create the database by running the following commands:
``` python manage.py makemigrations ```
``` python manage.py migrate ```

* Create a super user: ``` python manage.py createsuperuser ```

* Run the project: ``` python manage.py runserver ```

* Before logging in to the Django website make sure that Mailpit email client is running in your system to 
recieve an email activation link.

### To get started with this project with Docker:
* Make sure that Docker and docker-compose are installed in your system.

* Clone the repository: git clone https://github.com/MoustafaShaaban/Advanced_Django_Blog.git

* Change directory to blog_backend directory ``` cd blog_backend ```

* Build the docker image to develop the project locally using docker-compose:

``` docker-compose -f local.yml build ```

* Create the database by running the following commands:

` docker-compose -f local.yml run --rm django python manage.py migrate `

* Create a super user:

` docker-compose -f local.yml run --rm django python manage.py createsuperuser `

* Run the test using pytest:

``` docker compose -f local.yml run --rm django test blog_backend/blog ```

* Now run the project:

``` docker-compose -f local.yml up ```

* Open the web browser and go to ` http://localhost:8000/ ` to see the results.

* Start a new terminal and change directory to vue-frontend directory and install the requirements:

```bash

cd vue-frontend

npm install

```

* Run the Vue.js 3 frontend project:

```bash

    npm run dev

```


For more information about the available commands in this project check the Cookiecutter Django [Documentation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html#build-the-stack)


### References:

* [Django HTMX Modal Forms](https://blog.benoitblanchon.fr/django-htmx-modal-form/)

* [Django HTMX Toasts](https://blog.benoitblanchon.fr/django-htmx-toasts/)

* [Toast Up Your Django Messages with ToastifyJs](https://afeez1131.hashnode.dev/say-goodbye-to-dull-toast-up-your-django-messages-with-toastifyjs)

* [htmx in Django by examples](https://www.valentinog.com/blog/htmx-django-examples/)

* [Testing](https://www.valentinog.com/blog/testing-django/)

* [Date Field in Forms](https://mrasimzahid.medium.com/how-to-implement-django-datepicker-calender-in-forms-date-field-9e23479b5db)

* [How To Use the GitHub GraphQL API in Vue.js with Vue apollo](https://medium.com/@anoob.bava/how-to-use-the-github-graphql-api-in-vue-js-with-vue-apollo-24304b6731cf)

* [Django Session-based Auth for Single Page Apps](https://testdriven.io/blog/django-spa-auth/#setting-up-session-based-auth)

* [Building a CRUD client with Vue, TypeScript, vue-query](https://www.youtube.com/watch?v=JwS9nxwC1Vw)


### GraphQL Queries and Mutations Examples:

```gql

query ReturnAllPosts {
  allPosts {
    id
    title
    content
    updatedAt
    comments {
      id
      comment
      user {
        username
      }
    }
    tag {
      id
      name
    }
  }
}
```
-----------------------------------------------------------------------------

```gql

 query returnPostBySlug($slug: String!) {
      postBySlug(slug: $slug) {
        id
        title
        content
        author {
          username
          avatar
        }
        updatedAt
        comments {
          id
          comment
          user {
            username
          }
        }
        tag {
          id
          name
        }
      }
    }
```

and in the variables:
```js
{
"slug: "post-1"
}
```
-----------------------------------------------------------------------------
```gql
query ReturnMyPost {
  myPostsWithFilters {
    edges {
      node {
        id
        title
        content
        updatedAt
        comments {
          id
          comment
          user {
            username
          }
        }
        tag {
          id
          name
        }
      }
    }
  }
}
```
------------------------------------------------------------------------------
```gql
query PostByTitle {
  allPostsWithFilters(title: "Post Number 1") {
    edges {
      node {
        id
        title
        updatedAt
        content
        comments {
          id
          comment
        }
      }
    }
  }
}
```
--------------------------------------------------------------------------------
```gql
query AllComments {
  allComments {
    id
    user {
      name
    }
    comment
    post {
      id
      title
      content
      updatedAt
    }
  }
}
```
------------------------------------------------------------------------------
```gql
query AllTags {
  allTags {
    id
    name
    slug
  }
}
```
------------------------------------------------------------------------------
```gql
mutation createTag {
  createTag(input: {
    name: "Python"
  }) {
    tag {
      id
      name
    }
  }
}
```
------------------------------------------------------------------------------
```gql
mutation UpdateTag {
  updateTag(id: 1, name: "Python") {
    tag {
      id
      name
    }
  }
}
```
------------------------------------------------------------------------------
```gql
mutation DeleteTag {
  deleteTag(id: 6) {
    success
  }
}
```
------------------------------------------------------------------------------
```gql
mutation CreatePost {
  createPost(input: {
    title: "Post number 1",
    content: "Post number 1 content",
    tags: [
      { slug: "python" }
    ]
    
  }) {
    post {
      id
      content
    }
  }
}
```
------------------------------------------------------------------------------
```gql
mutation CreateComment {
  createComment(inputs: {
    postSlug: "post-1", 
    comment: "Great post", 
  }) {
    post {
      title,
      comments {
        comment
        user {
          username
        }
      }
    }
  }
}
```
---------------------------------------------------------------------------------
```gql
query PostsByAuthor {
  postsByAuthor(author: "admin") {
    id
    title
    updatedAt
    tag {
      name
    }
    content
    comments {
      id
      user {
        username
      }
      comment
    }
  }
}
```
---------------------------------------------------------------------------------
```gql
query PostsByTag {
  postsByTag(tag: "Python") {
    id
    title
    updatedAt
    tag {
      name
    }
    content
    comments {
      id
      user {
        username
      }
      comment
    }
  }
}
```
---------------------------------------------------------------------------------
```gql
query PostsByTitle {
  postByTitle(title: "Post number 1") {
    id
    title
    updatedAt
    tag {
      name
    }
    content
    comments {
      id
      user {
        username
      }
      comment
    }
  }
}
```
---------------------------------------------------------------------------------
```gql
query PostsByTitleWithDjangoFilters {
  allPostsWithFilters(title_Icontains: "Post number") {
   edges {
    node {
       id
        title
        updatedAt
        tag {
          name
        }
        content
        comments {
          id
          user {
            username
          }
          comment
        }
      }
    }
  }
}
```
---------------------------------------------------------------------------------
```gql
query PostsByTitleWithDjangoFilters {
  allPostsWithFilters(title_Istartswith: "Post number") {
   edges {
    node {
       id
        title
        updatedAt
        tag {
          name
        }
        content
        comments {
          id
          user {
            username
          }
          comment
        }
      }
    }
  }
}
```
---------------------------------------------------------------------------------
