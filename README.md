# Kanban Like Backend for Interview Applications

#### This application prepared for front end applicant for Smart Marine and Avatec Marine companies. For frontend users please check the section [Application Notes](#app_notes)

Contains:

API Level

1. User Registiration
1. User Authentication (with JWT)
1. Categories (CRUD)
1. Items (CRUD)

Websocket Level

1. Time
1. Notifications (Not Implemented Yet)
1. Changes (Not Implemented Yet)

<hr>

Contained Technologies

1. [Django](https://www.djangoproject.com/)
1. [Rest Framework](https://www.djangoproject.com/)
1. [Json Web Token](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
1. [Daphne Serving for ASGI](https://channels.readthedocs.io/en/stable/deploying.html)
1. [SQLite for Database](https://www.sqlite.org/index.html)

<hr>

Setup

## Due to rush, I couldn't fniish the installation yet. I install manually! THIS PART WILL BE COMPLETED AS THIS WAY!

```bash
$ git clone https://github.com/serkankas/django_kanban_backend.git
$ cd django_kanban_backend/
$ python3 install.py -i -d -n
```

<hr>

## Tasks

Build a simple web application that allows users to create and manage a list of tasks/items. Each task should have a title, description, and a category (e.g., "to do", "in progress", or "done").<br>
Tasks category should be able to be updated with drag and drop.<br>
Frontend should have modern design.<br>
Things you will need by the backend, such as API endpoints and database models, are given to you in advance.<br>
Connect given api endpoint with your web app<br>
Requirements:

The front-end should be built with React, using a state management library of your choice (e.g., Redux, MobX).<br>
The frontend must have Drag & Drop functionality <br>
The application should have the following functionality:<br>

The user can create its own account without validation. (For testing environment purposed.Not ideal)<br>
The user could sign in with their credentials.<br>
The user has to capture its own id from user list.<br>

The user should be able to create a new task by entering a category_id, title and description.<br>
The user should be able to view a list of all tasks, sorted by their category and order_id.<br>
The user should be able to update the category of a task (e.g., from "to do" to "in progress").<br>
The user should be able to delete a task.<br>
The application should have appropriate error handling and validation (e.g., preventing the user from submitting a blank title).<br>

The user should be able to create a new category by entering category title.<br>
The user should be able to view list of all categories he has, sorted by order_id.<br>
The user should be able to change the order of categories.<br>
The user should be able to delete the category/ies.<br>

The application should have appropriate styling using a CSS framework of your choice (e.g.,  Material UI). Preferred: Material UI

The code should be well-organized and documented.

You should include instructions for setting up and running the application locally.

<hr>

<section id="app_notes">

## Application Notes

In order to be precise I will gave as much information as possible for usage case.

Unlike standard Kanban Application with 3 status, This application written with categories and items. Categories corresponded for vertical blocks and items corresponded for horizontal blocks. It doesn't have to be 3, it can be more or less for desired application.

Application IP_Addresses : 134.209.207.128

### Token Authentication

Every API except 3 is need an token authentication<br>
Authentication should be set as follow in headers<br>
```Authorization: Bearer <access_token>```

The APIs that shouldn't use token:
1. /api/auth/token/get/
1. /api/auth/token/refresh/
1. /api/user/create/

AUTH-REASON: Token get and refresh gives an error if you implement expired token in it. So, be careful about this usage.<br>
USER-REASON: We want to applicant to create their own users for test purposes. NOT IDEAL Scenario.

### Models

We have 4 different model that we use in this application. Two of them is comes from library, two of them is created by this author.

|Model |Fields |Need2Know| CustomUsed|
|---|---|---|---
|Token |access_token |Yes |No
|Token |resresh_token |Yes |No
|User |username |Yes |No
|User |first_name |Yes |No
|User |last_name |Yes |No
|User |email |Yes |Yes
|User |password |Yes |No
|Category |id| Yes| Yes
|Category |category_id |Yes |No
|Category |category_title |Yes |No
|Category |order_id |Yes |Yes
|Category |created_date |No |No
|Category |user_accesses |No |Yes
|Item|id |Yes |Yes
|Item|item_id |Yes |No
|Item|item_title |Yes |No
|Item|item_description |Yes |No
|Item|order_id |Yes |Yes
|Item|created_date |No |No
|Item|owner |No |Yes
|Item|category |Yes |Yes

### APIs

For Request body or Response body, if else is not mentioned, the body itself is JSON objects. Written \<real_response>:\<actual_meaning> is given for hint. If any url contains \<something> you should write the actual_meaning value.

| Root URL| Sub Route| remain URL| any note| Method| Request Body| Response Body
| --- | --- | --- | --- | --- | --- | --- |
|http://134.209.207.128/api |/auth |/token/get/ | Used for accessing Token for first time. Shouldn't be used until the refresh token and access token both expire at the same time. | POST| username:user_username, password:user_password | access:access_token, refresh:refresh_token
|http://134.209.207.128/api |/auth |/token/refresh/ | if access token is expired, it should be called. If the refresh token is also expired then the new token should be requested. |POST| refresh:refresh_token| access:access_token, refresh:refresh_token
|http://134.209.207.128/api |/user |/list/ | listing users with their ids. Also could be used for if you successfully access | GET| none| list [user_id, user_username]
|http://134.209.207.128/api |/user | /get/\<user_id>/| This api will return the information about your user.| GET| none|  id:user_id, username:user_username, first_name:user_first_name, last_name:user_last_name
|http://134.209.207.128/api |/user | /create/| This is used for user creation| POST|username:user_username, password:user_password, first_name:user_first_name, last_name:user_last_name, email:user_email| message
|http://134.209.207.128/api |/user |/update/\<user_id>/| This api is used for changing user information except password| PUT|   id:user_id, username:user_username, first_name:user_first_name, last_name:user_last_name| message
|http://134.209.207.128/api |/user |/delete/<user_id>/ | This api used for user remove | DELETE| none| message/detail
|http://134.209.207.128/api |/user | /change_password/<user_id>/| Seperate api for changing user password| PUT/PATCH| id:user_id, username:user_username, password:user_password| message/detail
|http://134.209.207.128/api |/category | /list/| Getting current user categories| GET| none| message, categories={id:category_id_unique, category_id:category_id, category_title:category_title, order_id:category_order_id, created_date:category_created_date}
|http://134.209.207.128/api |/category |/get/\<category_id_unique>/ | Getting category list| GET| none| id:category_id_unique, category_id:category_id, category_title:category_title, order_id:category_order_id, created_date:category_created_date
|http://134.209.207.128/api |/category |/update/<category_id_unique>/ | Updating category information as well as ordering. The order will automatically update with this API| PUT/PATCH |category_title:category_title, order_id:category_order_id| message/detail
|http://134.209.207.128/api |/category | /create/| API for creating categories | POST | category_title:category_title| message
|http://134.209.207.128/api |/category | /delete/\<category_id_unique>/ | API for deleting category| DELETE| none| message/detail
|http://134.209.207.128/api |/item | /list/| API for getting user items.| GET| none| message, items:{id:item_id_unique, item_id:item_id, item_title:item_title, item_description:item_description, order_id:item_order_id, category_id:category_id_unique}
|http://134.209.207.128/api |/item | /get/\<item_id_unique>/| API for getting specific item information| GET |none| id:item_id_unique, item_id:item_id, item_title:item_title, item_description:item_description, order_id:item_order_id, created_date:item_created_date, owner_id:user_id, category_id:category_unique_id
|http://134.209.207.128/api |/item | /update/\<item_id_unique>/| API for changing item infos| PUT/PATCH| item_title:item_title, item_description:item_description, order_id:item_order_id, category_id:category_id_unique| message/detail
|http://134.209.207.128/api |/item | /create/| API for creating new item| POST| item_title:item_title, item_description:item_description, category_id:category_id_unique| message
|http://134.209.207.128/api |/item | /delete/\<item_id_unique>/| API for deleting an item| DELETE| none| message/detail

### Websocket

url: ws://134.209.207.128/ws/server_time/<br>
response: {date:\<date>, time:\<time>}

This is simple websocket application for testing websocket connection.

</section>