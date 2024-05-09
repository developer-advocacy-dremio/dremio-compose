# Kafka Connect Test Environment

## Step 1 - Configure Kafka Connect

Make sure the `iceberg-connector-config.properties` file has the right properties for your desired stream processing.

*The files in this repo already have default to work out of the box in this particular docker-compose environment*

iceberg-connector-config.properties
```properties
## Connector Settings
name=iceberg-sink-connector
connector.class=io.tabular.iceberg.connect.IcebergSinkConnector
tasks.max=2
topics=sales
iceberg.tables=streaming.sales

# Catalog Settings
iceberg.catalog.catalog-impl=org.apache.iceberg.nessie.NessieCatalog
iceberg.catalog.uri=http://nessie:19120/api/v2
iceberg.catalog.ref=main
iceberg.catalog.warehouse=s3a://warehouse
iceberg.catalog.s3.endpoint=http://minio:9000
iceberg.catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO
iceberg.catalog.client.region=us-east-1
iceberg.catalog.s3.path-style-access=true
iceberg.catalog.s3.access-key-id=admin
iceberg.catalog.s3.secret-access-key=password

## Other Settings
iceberg.control.commitIntervalMs=1000
```

kafka-connect.properties
```
# Kafka Connect basic settings
bootstrap.servers=kafka:29092
group.id=kafka-connect-group

# Key and value converters
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=false
value.converter.schemas.enable=false

# Internal topic names for storing configurations and offsets
config.storage.topic=kafka-connect-configs
offset.storage.topic=kafka-connect-offsets
status.storage.topic=kafka-connect-status

# Internal topic settings to ensure replication and durability
config.storage.replication.factor=1
offset.storage.replication.factor=1
status.storage.replication.factor=1

# Logging
errors.tolerance=all
errors.log.enable=true
errors.log.include.messages=true

# Plugin path
plugin.path=/usr/share/java

# Storage of Offset files
offset.storage.file.filename=/tmp/connect.offsets
schemas.enable=false
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

Once the nessie has been added as a source in Dremio.

- create a folder called `streaming` in your nessie source
- run the following sql to create your destination table 

```sql
CREATE TABLE nessie.streaming.sales (
    id VARCHAR,
    type VARCHAR,
    ts TIMESTAMP,
    payload VARCHAR)
PARTITION BY (hour(ts));
```

## Get Kafka-Connect Going

Run Kafka-Connect

```shell
docker compose up zookeeper kafka kafka-connect kafka-rest-proxy
```

Once these containers have started just populate the "sales" topic as stated in our connector configurations. There are two ways you can do this:

#### Using Kafka Rest Proxy

```shell
curl -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" \
     -H "Accept: application/vnd.kafka.v2+json" \
     --data '{
       "records": [
         {"value": {"id": 14, "product_name": "Smartphone", "quantity": 5, "price": 299.99}},
         {"value": {"id": 15, "product_name": "Tablet", "quantity": 2, "price": 450.00}},
         {"value": {"id": 16, "product_name": "Charging Cable", "quantity": 10, "price": 19.95}}
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
{"id": 101, "product_name": "Laptop", "quantity": 2, "price": 999.99}
{"id": 102, "product_name": "Smartphone", "quantity": 5, "price": 299.99}
{"id": 103, "product_name": "Keyboard", "quantity": 10, "price": 49.99}
```

Use `ctrl+c` to exit the console producer

- To confirm you added the records use the console consumer to bring them up

```shell
kafka-console-consumer --bootstrap-server localhost:9092 --topic sales --from-beginning
```