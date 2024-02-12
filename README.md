# HairHub
HairHub is a database and application backend that allows user to find hair salons.
There is a different interface for an admin, moderator and user.
Admin can add salons and services, but also can read opinions and reports.
Moderator can do all changes for his hair salon, like adding services from list and adding their prices and approximate time. He can also add worker and opneing hours.
User can search for hair salons by the name, address and services they offer. Later user can see details about specific salons and opinions, but can also add the salon to his list of favourite hair salons. User can add opinions and reports.

In order to make this work you have to create a folder which has: 
- compose.yaml
- folder named db
- folder named sql, which has the file backup2.sql

Our app runs on docker, so you have to enter the folder that you have created before and type in terminal: "docker-compose up -d".
After that you have to type: mysql -h 127.0.0.1 -u root -pYour_password
