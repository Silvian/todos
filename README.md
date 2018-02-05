# ToDos
### To-Do list project

The application provides APIs only. There is no web UI or client application for this service, only a stand-alone service with RESTful APIs.
 
The application must be able to:
-  Use username and password (or equivalent) to log in users
-  Use cookies (or effective alternative) to authenticate all API requests
-  Create a new to do item (containing a text description)
-  List a user’s set of to do items
-  Mark any single to do item as completed
-  Delete any single to do item
-  Log a user out
-  Run using Python 3.6 or higher
-  Use JSON for data exchange
 
### Considerations:
-  Creation of new users is out of scope.  The set of users can be hardcoded (at least one user)
-  The APIs should be RESTful
-  A quick, sure and repeatable proof that every element of the code works as intended, should be delivered alongside the service
-  Any libraries and frameworks can be used as long as they are publically available or included with the code.
 

### Installation Guide:

This project is dockerized so the following guide will highlight the requirements and steps needed
to run in a docker environment.

1. Install docker and docker-compose specific to your operating system. See https://www.docker.com for more details.

2. git clone the project and in the project base directory create a .env file with the following inside:

`DATABASE_HOST=postgres`

`DATABASE_NAME=postgres`

`DATABASE_USER=postgres`

`DATABASE_PASSWORD=postgres`

3. Inside the project base directory where docker-compose.yml file can be found, run the following commands:
#### docker-compose up --build

4. Once the process has finished and the postgres sql database and application are running,
run the migrations and load data command inside docker as following:
#### docker-compose run --rm web scripts/migrate_loaddata.sh

5. This also creates a default user: root with password: root

6. Login to the django administration page at: http://localhost:8000/admin/ with the credentials above to verify this.


Please visit http://localhost:8000/api/ for the API user guide django rest framework documentation and test web interface.

*Note:* you can login with the default user created here or create other users via django admin panel.
Any new users created must be given permissions to create/update/delete todo lists in the admin panel. 


### Testing:
To run the application test pack suite within docker container simply run:
#### docker-compose run --rm web python manage.py test
