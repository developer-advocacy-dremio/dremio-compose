# Dremio Docker-Compose Collection

If you just need Dremio and no other services you can spin it up with the following command:

```
docker run -p 9047:9047 -p 31010:31010 -p 45678:45678 -p 32010:32010 -e DREMIO_JAVA_SERVER_EXTRA_OPTS=-Dpaths.dist=file:///opt/dremio/data/dist --name try-dremio dremio/dremio-oss
```

This repository has collection of different docker-compose files for replicating different environments. If you have docker desktop on your machines you can use these files with the `docker-compose` or `docker compose` commands.

Assuming your terminal is in the same folder as a particular compose file:

- `docker compose up` run all services defined in the docker compose file

- `docker compose down` turn off all services in the docker compose file

- `docker compose up serviceName` turn on only a specified service from the docker compose file

- `docker compose down serviceName` turn off only a specified service from the docker compose file

- `docker compose exec serviceName command` run a command against a running a service

## Connecting the Nessie Catalog To Dremio

- Select Nessie as your new source

There are two sections we need to fill out, the **general** and **storage** sections:

##### General (Connecting to Nessie Server)
- Set the name of the source to “nessie”
- Set the endpoint URL to “http://nessie:19120/api/v2” 
Set the authentication to “none”

*"http://nessie" this namespace is determined by the service name in the docker compose yaml*

##### Storage Settings 
##### (So Dremio can read and write data files for Iceberg tables)

- For your access key, set “admin” (minio username)
- For your secret key, set “password” (minio password)
- Set root path to “warehouse” (any bucket you have access too)
    Set the following connection properties:
    - `fs.s3a.path.style.access` to `true`
    - `fs.s3a.endpoint` to `minio:9000`
    - `dremio.s3.compat` to `true`
- Uncheck “encrypt connection” (since our local Nessie instance is running on http)

*"minio:9000" this namespace is determined by the service name in the docker compose yaml*