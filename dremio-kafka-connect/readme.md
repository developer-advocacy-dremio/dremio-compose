# Kafka Connect Test Environment

## Step 1 - Configure Kafka Connect

Make sure the `iceberg-connector-config.properties` file has the right properties for your desired stream processing.

```properties
name=iceberg-sink-connector
connector.class=io.tabular.iceberg.connect.IcebergSinkConnector
tasks.max=2
topics=events
iceberg.tables=stream.sales
errors.tolerance=all
errors.log.enable=true
errors.log.include.messages=true

iceberg.catalog.catalog-impl=org.apache.iceberg.nessie.NessieCatalog
iceberg.catalog.uri=http://nessie:19120/api/v1
iceberg.catalog.ref=main
iceberg.catalog.warehouse=s3a://warehouse
iceberg.catalog.s3.endpoint=http://minio:9000
iceberg.catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO
iceberg.catalog.client.region=us-east-1
iceberg.catalog.s3.access-key-id=admin
iceberg.catalog.s3.secret-access-key=password
```

## Step 2 - Create Destination Table

Head to Localhost:9047 to create a nessie connection in dremio.

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