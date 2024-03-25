# Dremio Docker-Compose Collection

This repository has collection of different docker-compose files for replicating different environments. If you have docker desktop on your machines you can use these files with the `docker-compose` or `docker compose` commands.

Assuming your terminal is in the same folder as a particular compose file:

- `docker compose up` run all services defined in the docker compose file

- `docker compose down` turn off all services in the docker compose file

- `docker compose up serviceName` turn on only a specified service from the docker compose file

- `docker compose down serviceName` turn off only a specified service from the docker compose file

- `docker compose exec serviceName command` run a command against a running a service