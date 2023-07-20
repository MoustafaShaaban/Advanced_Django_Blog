# Advanced Django Blog

A Blog website built using [Django Web Framework](https://www.djangoproject.com/), [Django REST Framework](https://www.django-rest-framework.org), [Graphene Django](https://docs.graphene-python.org/projects/django/en/latest/) and [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django).

###  Project Goals

* Authenticated users can:

    * Access a GraphQL endpoint and run several Quries and CRUD Mutations.

    * Access a Rest API endpoint and run CRUD operations.

    * Create, Read, Update and Delete (CRUD) blog posts on the website.

    * Add comments on blog posts, but the comments will not be visiable until the website admin approves it.

    * Access their profile which lists all their blog posts and their favorite posts.

* All users can read or search for the posts on the blog.


### Project preview

* [Youtube](https://www.youtube.com/watch?v=mxe6Ca5yLOo)


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

* Throw a 403 forbidden page to any user who try to guss the URL to change something they are not authorized to do.

* Create a search form on your website.

* And many more.


### Libraries and Packages used

* [Django Web Framework](https://www.djangoproject.com/)

* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) package

* UI components from the official [Bootstrap 5.2](https://getbootstrap.com/docs/5.2/getting-started/introduction/) website documentation.


### To get started with this project

* Make sure that Docker and docker-compose are installed in your system.

* Clone the repository: git clone https://github.com/MoustafaShaaban/Advanced_Django_Blog.git

* Change directory to blog_backend directory ``` cd blog_backend ```

* Build the docker image to develop the project locally using docker-compose:

``` docker-compose -f local.yml build ```

* Create the database by running the following commands:

` docker-compose -f local.yml run --rm django python manage.py migrate `

* Create a super user:

` docker-compose -f local.yml run --rm django python manage.py createsuperuser `

* Now run the project:

``` docker-compose -f local.yml up ```

* Open the web browser and go to ` http://localhost:8000/ ` to see the results.


#### GraphQL Queries and Mutations Examples:

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
      email
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

-----------------------------------------------------------------------------

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
          email
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

------------------------------------------------------------------------------

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

--------------------------------------------------------------------------------

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

------------------------------------------------------------------------------

query AllTags {
  allTags {
    id
    name
    slug
  }
}

------------------------------------------------------------------------------

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

------------------------------------------------------------------------------

mutation UpdateTag {
  updateTag(id: 1, name: "Python") {
    tag {
      id
      name
    }
  }
}

------------------------------------------------------------------------------

mutation DeleteTag {
  deleteTag(id: 6) {
    success
  }
}

------------------------------------------------------------------------------

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

------------------------------------------------------------------------------

mutation {
  createComment(inputs: {
    postSlug: "post-1", 
    comment: "Great post", 
    email: "admin@admin.com"
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

---------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------


For more information about the available commands in this project check the Cookiecutter Django [Documentation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html#build-the-stack)
