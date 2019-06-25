# Surf Central
<hr>


Surf Central is a Twitter like application for surfing enthusiasts.<br>
Even though the site is currently under development, you can view the Staging site at the following address(built for Desktop):
> http://surf-central-stage.herokuapp.com/

The site currently supports the following functionality:
- Create and Edit posts.
- View user profiles for other members in the community.
- Follow your friends, and have their posts pop up in your feed!
- Access the API using the documentation below.


## Installation Instructions

If you want a local development copy for the project you can clone this repo.<br>
_The instructions assume you have a local Postgres Database with the name surf_db setup._<br>

Install the required packages using the **requirements.txt**
You can run the following command in your terminal in the project root with a virtual environment active(recommended):<br>
```sh
pip install -r requirements.txt
```

Follow that by exporting the following variables in your terminal instance:<br>
```sh
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/surf_db"
```

Make sure you are in the project root folder in your terminal and run the following command:

```sh
python blog_start.py
```
<br>
Proceed to "localhost:5000/" on your browser, and you should be able to access a local deployment of the site!

## API


| HTTP Method | Resource URL | Comments     |
| :---        |    :----:   |          ---: |
| GET         |`/api/users/<int:id>`| Return user info   |
| GET         |`/api/users`    | Return all users      |
| POST        |`/api/users?username=<>&password=<>`        | Reigster new user               |
| GET         |`/api/users/<int:id>/followers`            |Return followers for user               |
| GET         |`/api/users/<int:id>/followed`             |Return users followed by *id* user.               |

Pagination is employed for resources which return more than one object element.
