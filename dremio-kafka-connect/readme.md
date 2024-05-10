# Kafka Connect Test Environment

## Step 1: Configure Kafka Connect

Make sure the `iceberg-connector-config.properties` file has the right properties for your desired stream processing.

_The files in this repo already have a default to work out of the box in this particular docker-compose environment if you follow all the steps_

- **iceberg-connector-config.properties**: the iceberg connector configurations

- **kafka-connect.properties**: kafka connect global configurations

- **connect-log4j.properties**: Kafka Connect logging specific configurations

- **TransactionsData.json**: Sample Data

- **Dockerfile**: To rebuild Kafka-Connect image with configs and connector

- **docker-compose.yml**: details services available in environment
  - dremio: data lakehouse platform for querying data
  - nessie: iceberg catalog
  - minio: data lake object storage
  - minio-setup: service to preset the desired buckets in minio
  - kafka: message broker
  - zookeeper: needed by kafka
  - kafka-rest-proxy: A REST API interface for Kafka
  - kafka-connect: Kafka data integration framework (will write stream data to iceberg tables in nessie)

## Step 2: Spin up Environment

```bash
docker compose up -d minio minio-setup dremio nessie kafka kafka-rest-proxy
```

Once this is all setup you should be able to access minio on `localhost:9000` with these credentials:

- username: admin
- password: password

## Step 3: Add sample data

The settings in the repo use dynamic tables and uses "table" as the route field with autocreate tables. This means as records hit the "transactions" topic the records will be written to tables based on the value in that field. The connector will need to collect a bit of data to avoid writing overly small files so. For this demonstration we can can run the following curl request 20-30 times to give the kafka topic lots of information to be written.

```bash
curl -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" \
     -H "Accept: application/vnd.kafka.v2+json" \
     --data-binary "@./TransactionsData.json" \
     http://localhost:8082/topics/transactions
```

## Step 4: Run Kafka-Connect
To startup kafka connect run:

```bash
docker compose up --build kafka-connect
```

After the first time you run this, if you want to change any of the configurations change the string in this line in the `dockerfile` in order to break the cache and make sure docker copies over the newest version of your properties files:

```
# For breaking the cache at build time
RUN echo "hello ac"
```

Check minio periodically, you should see the tables being created and files being being written as you add more and more data to the "transactions" topic using our sample data.

## Step 5: Run Dremio

Head over to localhost:9047 and setup your Dremio account:

## Connecting the Nessie Catalog To Dremio

- Select Nessie as your new source

There are two sections we need to fill out, the **general** and **storage** sections:

##### General (Connecting to Nessie Server)

- Set the name of the source to “nessie”
- Set the endpoint URL to “http://nessie:19120/api/v2”
  Set the authentication to “none”

_"http://nessie" this namespace is determined by the service name in the docker compose yaml_

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

You should see all your tables in your new nessie source and your good to go query your data!