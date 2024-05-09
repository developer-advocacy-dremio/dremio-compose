# Kafka Connect Test Environment

## Step 1 - Configure Kafka Connect

Make sure the `iceberg-connector-config.properties` file has the right properties for your desired stream processing.

_The files in this repo already have a default to work out of the box in this particular docker-compose environment if you follow all the steps_

- **iceberg-connector-config.properties**: the iceberg connector configurations

- **kafka-connect.properties**: kafka connect global configurations

- **connect-log4j.properties**: Kafka Connect logging specific configurations

## Step 2 - Create Destination Table

```
docker compose up - dremio minio minio-setup nessie
```

Head to Localhost:9047 to create a nessie connection in dremio.

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

Once the nessie has been added as a source in Dremio.

- create a folder called `streaming` in your nessie source
- run the following sql to create your destination table

```sql
CREATE TABLE nessie.streaming.salesdata (
    id INT,
    customer_id INT,
    product_id INT,
    quantity INT,
    price DOUBLE,
    sales_timestamp TIMESTAMP,
    region VARCHAR
) PARTITION BY (HOUR(sales_timestamp));
```

## Get Kafka Going and Populate Topic

Run Kafka-Connect

```shell
docker compose up zookeeper kafka kafka-rest-proxy
```

### Creating the Required Topics

get into bash in the kafka container
```bash
docker exec -it kafka /bin/bash
```

create the topics

```bash
kafka-topics --create --topic sales --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

kafka-topics --create --topic iceberg-control --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
Once these topics have been created just populate the "sales" topic as stated in our connector configurations. There are two ways you can do this:

#### Using Kafka Rest Proxy

```shell
curl -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" \
     -H "Accept: application/vnd.kafka.v2+json" \
     --data '{
       "records": [
         {
           "value": {
             "id": 1,
             "customer_id": 101,
             "product_id": 501,
             "quantity": 2,
             "price": 19.99,
             "sales_timestamp": "2024-05-09T12:00:00Z",
             "region": "North America"
           }
         },
         {
           "value": {
             "id": 2,
             "customer_id": 102,
             "product_id": 502,
             "quantity": 1,
             "price": 99.99,
             "sales_timestamp": "2024-05-09T12:30:00Z",
             "region": "Europe"
           }
         },
         {
           "value": {
             "id": 3,
             "customer_id": 103,
             "product_id": 503,
             "quantity": 3,
             "price": 5.99,
             "sales_timestamp": "2024-05-09T13:00:00Z",
             "region": "Asia"
           }
         },
         {
           "value": {
             "id": 4,
             "customer_id": 104,
             "product_id": 504,
             "quantity": 1,
             "price": 299.99,
             "sales_timestamp": "2024-05-09T13:30:00Z",
             "region": "South America"
           }
         }
       ]
     }' \
     http://localhost:8082/topics/sales
```

#### Using Kafka CLI

- access the shell in the Kafka Container

```shell
docker exec -it kafka /bin/sh
```

- Open the console producer for the sales topic

```shell
kafka-console-producer --broker-list localhost:9092 --topic sales
```

- Begin entering JSON records and hit enter after each one to submit them

```json
{"id": 1, "customer_id": 101, "product_id": 501, "quantity": 2, "price": 19.99, "sales_timestamp": "2024-05-09T12:00:00Z", "region": "North America"}
{"id": 2, "customer_id": 102, "product_id": 502, "quantity": 1, "price": 99.99, "sales_timestamp": "2024-05-09T12:30:00Z", "region": "Europe"}
{"id": 3, "customer_id": 103, "product_id": 503, "quantity": 3, "price": 5.99, "sales_timestamp": "2024-05-09T13:00:00Z", "region": "Asia"}
{"id": 4, "customer_id": 104, "product_id": 504, "quantity": 1, "price": 299.99, "sales_timestamp": "2024-05-09T13:30:00Z", "region": "South America"}
```

Use `ctrl+c` to exit the console producer

- To confirm you added the records use the console consumer to bring them up

```shell
kafka-console-consumer --bootstrap-server localhost:29092 --topic sales --from-beginning
```

## Step 3 - Startup Kafka Connect

```
docker compose up kafka-connect
```

and well... it should just work!