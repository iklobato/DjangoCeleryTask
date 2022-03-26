# DjangoCeleryTask

This is a project to test the integration between Django Rest Framework and Celery, in which a payload with user id is received at the /celery_ids_tasks/ endpoint and the api executes them asynchronously.

This application receives a POST with an enumerated list with IDS of users, processes them and organizes them in an API in a database so that it can be retrieved at any time.

### How to run the application
```shell
docker-compose up -d
```
And then, you can access the application at:
```shell
http://0.0.0.0:8000/
```
Expected output
- <img width="656" alt="Screen Shot 2022-03-25 at 23 54 15" src="https://user-images.githubusercontent.com/18133417/160222123-fea951f5-0b68-4ad3-b39d-492edd6ae6b4.png">


### Organization logic of received IDs
As the IDs are received every second, the logic goes like this:
- The hour is divided into 4 parts, minutes 15, 30, 45 and 60
- Each hour grouping has a maximum number of requests per minute to be made, as the minutes are separated by ID groupings
- The rule adding people to groups follows consecutively until all groups are at their maximum capacity.
- After no more people (IDs) can fit in the minute groups, the rule follows the rule of dissipating the new IDs received in every minute so that there is no processing peak.
- Another detail is that the algorithm that distributes the IDs between the different minutes is a python generator, that is, regardless of the size of the IDs that are passed, memory is not used for storage in Runtime, only when it is requested the *next()* for the next number.

An example:
If we define an RPM (request per minute) of 5 ids we will have a maximum grouping of 5 people per minute. Following the first rule we will then have
- <img width="463" alt="Screen Shot 2022-03-25 at 18 37 26" src="https://user-images.githubusercontent.com/18133417/160204778-d358246e-aefa-45af-96b6-3a27c679e8b8.png">

If we are following the second logic, we will dispersely fill in the IDs as shown in the example to the side, but it will only happen if the groups are already at their maximum RPM capacity and new IDs still need to be added.
- <img width="558" alt="Screen Shot 2022-03-25 at 18 39 58" src="https://user-images.githubusercontent.com/18133417/160205205-29d3b27f-5472-495d-8b11-038d23ade918.png">

Here we have a better one with maximum capacity like MAX=2.
After each value has been filled sequentially the first time, the algorithm after filling goes to the second strategy which is dispersed. Here we can see 1002 and 1002 in the same group, up to 1029 and 1030. After that, as the maximum amount of the group of 2 is reached, the rule is to disperse the new IDs in a pulverized way.
- <img width="464" alt="Screen Shot 2022-03-25 at 18 42 13" src="https://user-images.githubusercontent.com/18133417/160205963-ffa3ffb0-637f-4eb2-a6eb-f1d46cb290c5.png">

## Endpoints
Get the list of all users received by IDs

### Users
```
GET /users/
```
Create a new user
```
POST /users/
```
Update user
```
PUT /users/<id>/
```
Update user field
```
PATCH /users/<id>/
```
### IDs tasks
Get the list of all tasks scheduled in the system.
```
GET /celery_ids_tasks/
```
Sends IDs to be saved and calculated asynchronously by the backend.
```
POST /celery_ids_tasks/
```
Update task
```
PUT /celery_ids_tasks/
```
Partial update task field
```
PATCH /celery_ids_tasks/
```

## Core files to check
Models
- https://github.com/henriqueblobato/DjangoCeleryTask/blob/master/api/models.py

Views
- https://github.com/henriqueblobato/DjangoCeleryTask/blob/master/api/views.py

Serializers
- https://github.com/henriqueblobato/DjangoCeleryTask/blob/master/api/api/serializers.py

Business logic to insert IDs on the minute queues
- https://github.com/henriqueblobato/DjangoCeleryTask/blob/master/tasks/logica.py

Hour checker to the minutes 0, 15, 30 and 45
- https://github.com/henriqueblobato/DjangoCeleryTask/blob/master/tasks/hour_checker.py

Putting request tasks at the Celery background
- https://github.com/henriqueblobato/DjangoCeleryTask/blob/master/tasks/task_test.py
