# Simple Bulk Transfer

This folder explains how you can implement a bulk transfer from a MySql database to MySql Database.

### Flow (Bulk Transfer):
**Source Data (MySql) ---> Kafka Topic ---> Destination Data (MySql)**

---
### Use-Case:

- For this use-case I had a very simple example wherein I wanted to have a source table which consists of columns like id, name and role.
- All I wanted to do was to write some data into the source table and that data should be extracted to the Kafka Topic regularly which means pull the whole data in the Topic and then in the final destination table i'll be pulling the data from the topic.

### Steps to follow:

- Make sure you have configured docker properly.

- **Creating docker-compose file**

- [Refer this file]() to understand which services I've used for this use case.

1. **mysql**

    a. `image`: Docker will pull this image from Docker Hub (if not already available locally). As per our file, it will pull *MySQL 8.0*.

    b. `container_name`: This sets the name of the container created from this service to **mysql**.

    c. `privileged`: This grants the container elevated privileges (similar to root access) inside the container. (not recommended though).

    d. `environment`: This section allows you to pass environment variables to the container mainly for mysql configuration like: `MYSQL_ROOT_PASSWORD` (sets the root password for the MySQL database), `MYSQL_DATABASE` (sets the name of the database for which you'll be working)

    e. `ports`: This allows you to access the MySQL service from your host machine using port *3307* instead of the default port *3306*. For example, if you want to connect to the MySQL server from a MySQL client, you would connect to `localhost:3307`.


2. **zookeper**

    a. `image`: Docker will pull this image from Docker Hub (if not already available locally). As per our file, it will pull *confluentinc/cp-zookeeper:5.0.0*, the image for Zookeeper provided by Confluent, a company that provides a Kafka ecosystem, including Zookeeper, Kafka, and related tools

    b. `container_name`: This sets the name of the container created from this service to **zookeper**.

    c. `privileged`: This grants the container elevated privileges (similar to root access) inside the container. (not recommended though).

    d. `ports`: This defines the port mapping between the container and the host machine. `2181:2181` means that the container’s port 2181 (the default Zookeeper client port) is exposed on the host’s port 2181.

    e. `environment`: This sets environment variables that configure the behavior of the Zookeeper container when it starts up. The configs i've done are `ZOOKEEPER_CLIENT_PORT` (the port on which Zookeeper will listen for client connections) and `ZOOKEEPER_TICK_TIME` (how quickly Zookeeper should detect failures and how long it should wait for other nodes to respond)

3. **kafka**:

    a. `ports`: Kafka clients or applications running on your local machine (or network) can connect to the Kafka broker via localhost:9092

    b. `links`: This creates a link between the Kafka container and the Zookeeper container. Essentially, it makes the Zookeeper container accessible to Kafka under the alias zookeeper.

    c. `environment`: This sets environment variables to configure Kafka. `KAFKA_ZOOKEEPER_CONNECT` (tells Kafka where to find the Zookeeper instance it needs to connect to. Kafka uses Zookeeper for coordination and management of distributed nodes.), `KAFKA_ADVERTISED_LISTENERS` (Kafka is advertising itself to clients as being available at the hostname kafka (the name of the Kafka container) on port 9092.), `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR` (sets the replication factor for the offsets topic to 1. This means that the offsets topic will not be replicated across multiple Kafka brokers; it will only have a single replica.)

4. **kafka-connector-mysql**
    a. `ports`: *8083:8083* Exposes Kafka Connect's REST API on port 8083, allowing management of connectors via localhost:8083.

    b. `links`: Links the Kafka, Zookeeper, and MySQL containers to allow Kafka Connect to communicate with these services by their container names (kafka, zookeeper, mysql).

    c. `environment`: `CONNECT_BOOTSTRAP_SERVERS` (Tells Kafka Connect where to find the Kafka broker (via kafka:9092)).
    `CONNECT_REST_PORT` (Sets the REST API port for Kafka Connect),
    Internal Kafka topics (`CONNECT_CONFIG_STORAGE_TOPIC`, `CONNECT_OFFSET_STORAGE_TOPIC`, `CONNECT_STATUS_STORAGE_TOPIC`) manage connector configs, offsets, and statuses.
    `CONNECT_KEY_CONVERTER` and `CONNECT_VALUE_CONVERTER`: Use JSON for data serialization.
    `CONNECT_LOG4J_ROOT_LOGLEVEL`: DEBUG: Enables debug logging for troubleshooting.
    `CONNECT_PLUGIN_PATH`: "/etc/kafka-connect/jars": Directory for Kafka Connect plugins (e.g., MySQL connector).

5. **control-center**

    a. `ports`: Exposes port 9021 of the container to port 9021 on the host machine. This allows you to access the Control Center web UI at http://localhost:9021.

    b. `links`: Establishes network links between the Control Center container and the Zookeeper and Kafka containers. These links make Zookeeper (zookeeper:2181) and Kafka (kafka:9092) accessible by their container names.
    
    c. `environment`:These environment variables configure the behavior of Control Center.

    `CONTROL_CENTER_BOOTSTRAP_SERVERS`: Specifies the Kafka broker to connect to (kafka:9092).
    `CONTROL_CENTER_ZOOKEEPER_CONNECT`: Specifies where Control Center can find Zookeeper (zookeeper:2181).
    `CONTROL_CENTER_CONNECT_CLUSTER`: kafka-connector-mysql: Indicates the name of the Kafka Connect cluster to monitor (kafka-connector-mysql).
    `CONTROL_CENTER_INTERNAL_TOPICS_PARTITIONS`: Sets the number of partitions for internal topics used by Control Center (usually for performance tuning).
    `CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS`: Defines the partition count for the monitoring interceptor topics.
    `CONTROL_CENTER_GROUP_TOPIC_PARTITIONS`: Sets the partition count for the group topics (used for tracking consumer group statuses).
    `CONTROL_CENTER_INTERNAL_TOPIC_REPLICATION`: Specifies the replication factor for internal topics (set to 1 for simplicity, typically higher in production).
    `CONTROL_CENTER_COMMAND_TOPIC_REPLICATION`: Sets the replication factor for command topics used by Control Center.
    `CONTROL_CENTER_CONTROL_TOPIC_REPLICATION`: Sets the replication factor for control topics.
    `CONTROL_CENTER_SAFETY_VALVE_TOPIC_REPLICATION`: Configures replication factor for safety valve topics used for system resilience.
    `CONTROL_CENTER_ZOOKEEPER_TIMEOUT_MS`: Sets the timeout for Zookeeper connections (in milliseconds, 10 seconds here).
    `CONTROL_CENTER_ZOOKEEPER_CONNECT_TIMEOUT_MS`: Sets the connection timeout for Zookeeper (also 10 seconds).
    `CONTROL_CENTER_REPLICATION_FACTOR`: Sets the replication factor for topics managed by Control Center (set to 1 for simplicity).

- Now, that you've configured everything that we need for this use-case, it's time to start the container.

- Run `docker-compose up -d` command in the terminal.

- The Above command will start the container with all the images as mentioned in the `docker-compose` file.

- Verify whether the container has started running (under container tab) by opening the Docker Desktop Application.

```json
{
    "name": "quickstart-jdbc-source",
    "config": {
      "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
      "tasks.max": 1,
      "connection.url": "jdbc:mysql://mysql:3306/kafkaa_test",
      "connection.user": "root",
      "connection.password": "root",
      "mode": "bulk",
      "table.whitelist" : "kafkaa_test.source_table",
      "error.tolerance": "all",
      "errors.log.enable" : "true",
      "topic.prefix": "quickstart-jdbc-",
      "poll.interval.ms": 1000
    }
  }
```


```json
{
  "name": "quickstart-jdbc-sink",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:mysql://mysql:3306/kafkaa_test",
    "connection.user": "root",
    "connection.password": "root",
    "topics": "quickstart-jdbc-source_table",
    "insert.mode": "upsert",
    "auto.create": "false",
    "auto.evolve": "true",
    "batch.size": "1000",
    "max.retries": "10",
    "retry.backoff.ms": "5000",
    "key.ignore": "true",
    "table.name.format": "sink_table",
    "pk.mode": "record_value",
    "pk.fields": "id"
  }
}
```