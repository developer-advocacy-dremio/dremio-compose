## Environment Setup

Before spinning environment, place any desired sample data in the sample data folder.

- Spin up `docker compose up`

- Spin down `docker compose down`

## Connecting Lake to Dremio

After a few minutes you should be able to access Dremio from http://localhost:9047

After setting up an account we will add 3 sources:

- Nessie sources that will save tables to "warehouse" bucket

- S3 source that you can use to write tables to "lakehouse" bucket

- S3 source to access sample data from

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

## Configuring S3/Minio Sources

### For Lakehouse Bucket

Choose S3 Source

**GENERAL SETTINGS**
- name: lakehouse
- credentials: aws access key
- accesskey: admin
- secretkey: password
- encrypt connection: false

**ADVANCED OPTIONS**
- enable compatibility mode: true
- root path: /datalakehouse
- Connection Properties
    - fs.s3a.path.style.access = true
    - fs.s3a.endpoint = storage:9000

### For Sample Data

Choose S3 Source

**GENERAL SETTINGS**
- name: sampledata
- credentials: aws access key
- accesskey: admin
- secretkey: password
- encrypt connection: false

**ADVANCED OPTIONS**
- enable compatibility mode: true
- root path: /sampledata
- Connection Properties
    - fs.s3a.path.style.access = true
    - fs.s3a.endpoint = storage:9000