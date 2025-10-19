# Virtual Workspace Room Booking System

GitHub-URL: 
https://github.com/ChiggyJain/PythonVirtualWorkSpaceRoomBookingSystem

Explaination Of Project Directory:
1) /api/v1/: Contains files related to endpoints, db-queries, schemas etc...
2) /core/mysql_db.py: This file contains related to singleton-db-connection.
3) /db/dump_data.sql.py: This file contains VIRTUAL_WORKSPACE db initialize with dummy data.
4) /utils/utils/py: This file contains generalize utils which required in this project
5) /.gitignore: This file contains ignoring some file and folder while commiting to git.
6) /docker-compose_production_machine.yaml: This is docker compose file for building/intialize the container/services example: mysqldb, app
7) /Dockerfile_production_machine: This is dockerfile for building the docker-image
8) /requirements.txt: This file contains the dependency of this project

Endpoints Explaination:
1) http://127.0.0.1:8001/api/v1/login/
POST: This api is used to login into the system and get access-token
2) http://127.0.0.1:8001/api/v1/teams/
GET: This api is used to get all teams with members count details
3) http://127.0.0.1:8001/api/v1/rooms/available
GET: This api is used for check available rooms for booking on given access-token, room-type, date-time slot.
4) http://127.0.0.1:8001/api/v1/bookings/
POST: This api is used for creating room booking details based on team/individual-user.
5) http://127.0.0.1:8001/api/v1/cancel/
POST: This api is used for cancelling booked room booking.
6) http://127.0.0.1:8001/api/v1/booking/
GET: This api is used for get all booked/cancelled room booking list details.


How to execute this project into your local machine:
Step1: Run this command into terminal
sudo systemctl stop mysql
Step2: 
mkdir PythonVirtualWorkSpaceRoomBookingSystem
git clone https://github.com/ChiggyJain/PythonVirtualWorkSpaceRoomBookingSystem.git 
Step3: Run this command into project directory
docker compose -f docker-compose_local_machine.yaml down -v
docker compose -f docker-compose_local_machine.yaml build --no-cache
docker compose -f docker-compose_local_machine.yaml up
Step4: Run this url into browser
http://127.0.0.1:8001/docs




