<h1> Library Service API 📚 📕 📖 </h1>

<h3> This project is an online management system for book borrowings.</h3>

<ul>
   <li>This system optimizes the work of library administrators.</li>
   <li>Makes the service much more user-friendly</li>
</ul>

## My Trello Board on this project:
[![My Trello board](https://img.shields.io/badge/View%20on%20Trello-blue?style=flat&logo=trello)](https://trello.com/invite/b/W7LF84Dd/ATTI83b1887d243c10938fcf62648b04dfb5169BD2EB/library-service-api)

## Project Features:

### Books Service:
- **CRUD Functionality:** Allows adding, viewing, updating, and deleting book records through the Books Service.
- **Permissions:** Only administrators can create, update, and delete books. All users, including unauthenticated ones, can see the list of books.
- **JWT Token Authentication:** Uses JWT tokens for secure user authentication.

### Users Service:
- **CRUD Functionality:** Allows adding, viewing, updating, and deleting book records through the Users Service.
- **JWT Support:** Supports JWT tokens for secure user authentication.

### Borrowings Service:
- **Create Borrowing Endpoint:** Enables users to borrow books with checks for available inventory and user association.
- **Filtering:** Non-admin users can only view their own borrowings, enhancing privacy and security.
- **Return Borrowing Functionality:** Implements the ability to return borrowed books while ensuring it cannot be done more than once and updates book inventory accordingly.
- **Notifications:** Sends notifications via Telegram API for each new borrowing.
- **Telegram Integration:** Sets up communication with Telegram for sending notifications.

### ModHeader Integration:
- **Chrome Extension Compatibility:** Enhances user experience with the ModHeader Chrome extension by customizing the default Authorization header to Authorize for JWT authentication.

### API Documentation (Spectacular Integration):
- **Swagger UI:** Provides interactive API documentation at `/api/doc/swagger/`.
- **Redoc UI:** Offers clear and readable API documentation at `/api/doc/redoc/`.
- **Schema Endpoint:** Accesses the API schema at `/api/schema/`.


## Stages of Project Creation:
<ul>
    <li>Initialization of the project</li>
    <li>Creating the Books service</li>
    <li>Creating service users</li>
    <li>Adding access rights to the Books service</li>
    <li>Creating a Borrowings service</li>
    <li>Implementation of Borrowing functionality creation</li>
    <li>Implementation of Borrowings filtering and List endpoint</li>
    <li>Implementation of the Borrowing return functionality</li>
    <li>Implementation of tests for Borrowing and Book</li>
    <li>Documentation of the project</li>
    <li>Integration of sending notifications when creating a Borrowing</li>
    <li>Registration of models in the admin panel</li>
    <li>Update README.md</li>
</ul>


## Test Coverage Report:

```plaintext
Name                                                                    Stmts   Miss  Cover
-------------------------------------------------------------------------------------------
books\__init__.py                                                           0      0   100%
books\admin.py                                                              3      2    33%
books\apps.py                                                               4      0   100%
books\migrations\0001_initial.py                                            5      0   100%
books\migrations\__init__.py                                                0      0   100%
books\models.py                                                            12      1    92%
books\permissions.py                                                        4      0   100%
books\serializers.py                                                        6      0   100%
books\tests\__init__.py                                                     0      0   100%
books\tests\test_book_api.py                                               72      0   100%
books\urls.py                                                               6      0   100%
books\views.py                                                              8      0   100%
borrowings\__init__.py                                                      0      0   100%
borrowings\admin.py                                                         7      6    14%
borrowings\apps.py                                                          4      0   100%
borrowings\migrations\0001_initial.py                                       7      0   100%
borrowings\migrations\0002_borrowing_borrow_date_not_past_and_more.py       7      0   100%
borrowings\migrations\0003_remove_borrowing_borrow_date_not_past.py         4      0   100%
borrowings\migrations\__init__.py                                           0      0   100%
borrowings\models.py                                                       27      2    93%
borrowings\serializers.py                                                  44      0   100%
borrowings\tests\__init__.py                                                0      0   100%
borrowings\tests\test_borrowing_api.py                                    137      0   100%
borrowings\urls.py                                                          6      0   100%
borrowings\views.py                                                        49      0   100%
library_service_api\__init__.py                                             0      0   100%
library_service_api\settings.py                                            26      0   100%
library_service_api\urls.py                                                 4      0   100%
manage.py                                                                  12      2    83%
telegram_api\__init__.py                                                    0      0   100%
telegram_api\telegram_helper.py                                            12      2    83%
users\__init__.py                                                           0      0   100%
users\admin.py                                                             12     11     8%
users\apps.py                                                               4      0   100%
users\migrations\0001_initial.py                                            7      0   100%
users\migrations\__init__.py                                                0      0   100%
users\models.py                                                            36      8    78%
users\serializers.py                                                       17      7    59%
users\tests\__init__.py                                                     0      0   100%
users\tests\test_user_api.py                                                0      0   100%
users\urls.py                                                               5      0   100%
users\views.py                                                             13      1    92%
-------------------------------------------------------------------------------------------
TOTAL                                                                     560     42    92%
```

## Installation and Usage:
<ul>
    <li>Python3 must be already installed</li>
    <li>Clone the repository.</li>
    <li>Set up environment variables using `.env.sample` as a guide.</li>
    <li>Run the application.</li>
    <li>Feel free to explore and contribute!</li>
</ul>

```shell
git clone https://github.com/o-davydova/Library-Service-API
cd Library-Service-API

python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

set DJANGO_SECRET_KEY=<your django secret key>
set DJANGO_ALLOWED_HOSTS=<your allowed hosts>
set DJANGO_DEBUG=<your debug value>

set TELEGRAM_BOT_TOKEN=<your telegram secret key>
set TELEGRAM_CHAT_ID=<your telegram chat id>

python manage.py migrate
python manage.py runserver
```

## Getting access:
- create a user via **/api/user/register**
- get access token via **/api/user/token**
