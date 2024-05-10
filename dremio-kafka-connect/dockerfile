# Use the base Kafka Connect image
FROM confluentinc/cp-kafka-connect:latest

# Set the working directory
WORKDIR /usr/share/java

# Download and install the Apache Iceberg Kafka Connect Sink
# This step assumes you have the connector jar available at a certain URL or locally.
COPY ./iceberg-kafka-connect-runtime-0.6.16 /usr/share/java/kafka-connect-iceberg/

# For breaking the cache at build time
RUN echo "hello ac"

# (Optional) Add your Kafka Connect configuration files

COPY ./kafka-connect.properties /etc/kafka-connect/config/
COPY ./iceberg-connector-config.properties /etc/kafka-connect/config/

# granular logging for troubleshoot
# COPY ./connect-log4j.properties /etc/kafka/

# Set up the environment variables or any additional setup steps
ENV CONNECT_PLUGIN_PATH="/usr/share/java/kafka-connect-iceberg,/usr/share/java/kafka-connect-jdbc"

# Expose the necessary port numbers
EXPOSE 8083

# Run the Kafka Connect worker
CMD ["/bin/connect-standalone", "/etc/kafka-connect/config/kafka-connect.properties", "/etc/kafka-connect/config/iceberg-connector-config.properties"]
