# Task Management System

Submitted by
Name: Wasikur Rahman
email: tawhidwasik08@gmail.com

## Table of Contents

- [Installation](#installation)
- [Usage & Features](#usage--features)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tawhidwasik08/drf-task-manager.git
2. Create a new virtual environment
    ```bash
   python3 -m venv tms_venv
3. Activate the virtual environment. (For windows)
    ```bash
    tms_venv\Scripts\activate.bat
4. Install the project dependencies. 
    ```bash
    pip install -r requirements.txt
5. Move to backend/ directory
    ```bash
    cd backend
6. Setup database
    ```bash
    python manage.py makemigrations
    python manage.py migrate
7. Run the server
    ```bash
    python manage.py runserver
* The API should now be accessible at `http://localhost:8000/`
* __Admin panel should checked for different user role tokens at `http://localhost:8000/admin/`__
    * Superuser name:su_admin_01 , password:12345
    *  If any superuser is non existent. Run `python manage.py test createsuperuser` from `/backend/`
## Usage & Features
* Users
    * Users can be created freely with any of the 3 roles - admin, manager, team_member. Authentication is not implemented at registration to avoid demo showing complexity.
    * Admin has access to everything except for updating any comment.
    * Manager has access to -
        * Getting all users info
        * Creating, updating, deleting Tasks and task comments
        * Getting info of tasks of which he is the creator
        * Assigning team_members to a task by updating the task
    * Team member has access to
        * Creating, updating and deleting task comments
    * Access token for each user will be generated at registration.

* Tasks
    * Creator will be auto assigned by the user who is currently authorized 
    * Can be filtered through:
        * Assigned to a user_id, completed or not, due date
        * Sort descending or ascending by due date, task id, priority

* Task Comments
    * Only admin or the creator of the comment can update or delete it.
    * Admin, Task Creator Manager or Task Assignees can only comment on a given task.

* Others
    * Pagination is done by LimitOffsetPagination. Limit and offset parameters are given in available endpoints.
    * There are 28 test cases. Run `python manage.py test` from `/backend/`
    * There is a data generator script. Run `python data_generator.py` from `/backend/`

        


## API Documentation
The API documentation is available at [Swagger UI](http://localhost:8000/swagger/) for detailed information about the endpoints and request/response formats.


## API Endpoints
| Method | Endpoint | Function | Role Permission |
|--------|----------|----------|-----------------|
| GET    | /users/ | get multi/single user info | Admin, Manager |
| POST   | /users/ | create new user | Unauthorized |
| GET    | /tasks/ | get tasks info | All |
| POST   | /tasks/ | create a task | Admin, Manager |
| GET    | /tasks/{task_id}/ | get single task info | All |
| PATCH  | /tasks/{task_id}/ | update task | Admin, Manager |
| DELETE | /tasks/{task_id}/ | delete task | Admin, Manager |
| GET    | /task-comments/ | get task_comments | All |
| POST   | /task-comments/ | create task_comments | All |
| GET    | /task-comments/{comment_id}/ | get single task_comment info | All |
| PATCH  | /task-comments/{comment_id}/ | update a task_comment | All |
| DELETE | /task-comments/{comment_id}/ | delete a task_comment | All |
