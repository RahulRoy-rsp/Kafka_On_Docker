# Change Data Capture (CDC)

- This folder explains how you can use **KSQL** for transformation.
- In short,  stream tables from Postgres to Kafka/KSQL back to Postgres
- I've referenced this article: [Article_Link](https://www.highalpha.com/blog/data-stream-processing-for-newbies-with-kafka-ksql-and-postgres)
- You can also find the github repo for the above implementation: [Github_Link](https://github.com/mtpatter/postgres-kafka-demo)

---

### Steps to Follow:

1. Make sure you have installed & configured docker properly.

2. **Creating docker-compose file**
     - The services that we need for this use-case are *postgres, kafka, zookeeper, ksql-server, schema-registry, connect (debezium).* 
    - `postgres` is the database we will be using for the tables.
    - `kafka` is used as the distributed streaming platform.
    - `zookeper` is used for distributed services that helps manage kafka's cluster.
    - `ksql-server` is used for real time updates.
    - `schema-registry` is used for managing AVRO schemas used by Kafka *Producers* and *Consumers*.
    - `connect` which is pulled from `debezium` for change data capture, which streams data change.
    - [Refer this file](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_4/docker-compose.yml).

3. Start the container will all the services in the `docker-compose` file.
    - The below command will start the container with all the images as mentioned in the `docker-compose` file.
    ```bash
    docker-compose up -d
    ```
    - Verify whether the container has started running (*under container tab*) by opening the Docker Desktop Application.
    - OR by using the below command:
    ```bash
    docker ps
    ```

4. Now log into postgres cli for *creating databases, tables and inserting values into the tables*.
    - The below command is the general syntax for logging into postgres.
    ```bash
    docker run -it --rm --network=<folder_name>_default postgres:11.0 psql -h <hostname> -U <username>
    ```
    Since I had used folder name as `Use_Case_4`
    ```bash
    docker run -it --rm --network=Use_Case_4_default postgres:11.0 psql -h postgres -U postgres
    ```
    - And then create a database and connect to it
    ```sql
    CREATE database students;
    \connect students;
    ```
    - Alternatively, you can also use `psql -U <username> -d <database_name>`

5. Set some configurations for postgres
    1. **`ALTER SYSTEM SET log_min_error_statement = 'fatal';`**
        - Sets the minimum error level to log fatal errors only, reducing log verbosity.

    2. **`ALTER SYSTEM SET log_min_messages = 'DEBUG1';`**
        - Configures logging to include detailed debug-level messages for troubleshooting.

    3. **`ALTER SYSTEM SET listen_addresses = '*';`**
        - Allows PostgreSQL to listen on all network interfaces, enabling remote connections.

    4. **`ALTER SYSTEM SET shared_preload_libraries = 'decoderbufs,wal2json';`**
        - Loads libraries necessary for logical replication and change data capture (CDC) with Debezium.

    5. **`ALTER SYSTEM SET wal_level = 'logical';`**
        - Enables logical replication by setting the WAL level to logical, required for CDC.

    6. **`ALTER SYSTEM SET max_wal_senders = 1;`**
        - Limits the number of concurrent WAL sender processes to 1, used in replication.

    7. **`ALTER SYSTEM SET max_replication_slots = 1;`**
        - Sets the maximum number of replication slots to 1, which is needed for logical replication.

    8. **`ALTER SYSTEM SET track_commit_timestamp = 'on';`**
        - Enables tracking commit timestamps for transactions, which is essential for CDC.

    9. **`SELECT pg_reload_conf();`**
        - Reloads the PostgreSQL configuration to apply changes without restarting the server.

    Set the below configurations:
    ```sql
    ALTER SYSTEM SET log_min_error_statement = 'fatal';
    ALTER SYSTEM SET log_min_messages = 'DEBUG1';
    ALTER SYSTEM SET listen_addresses = '*';
    ALTER SYSTEM SET shared_preload_libraries = 'decoderbufs,wal2json';
    ALTER SYSTEM SET wal_level = 'logical';
    ALTER SYSTEM SET max_wal_senders = 1;
    ALTER SYSTEM SET max_replication_slots = 1;
    ALTER SYSTEM SET track_commit_timestamp = 'on';
    ```

6. Create tables and insert values into the tables.
