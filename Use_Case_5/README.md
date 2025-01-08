# Timestamp + Incrementing Mode Transfer (Additionally Schema Evolution) 

This folder showcases how you implement `timestamp+incrementing` mode of transfer, plus `automatic table creation` in the destination database and `schema evolution` when processing the data across the source and destination table.

### Key configuration Options
 - **"mode": "timestamp+incrementing"**
    - In the source connector configuration, we specify the mode as **`"timestamp+incrementing"`**. 
    - This mode allows the connector to use both:
        - A **timestamp column** to track when the data was last modified or created.
        - An **incrementing column** (typically the primary key) to identify the last processed record.

 - **"timestamp.column.name": "<timestamp_column>"**
    - This option specifies the name of the **timestamp column** in the source table that the connector uses to track changes. 
    - The column should be of a `TIMESTAMP` or `DATETIME` type that records the last modification time of a record.
    - **Only updates the destination table when the updated data is ahead of what currently lies in the destination table.**
    
 - **"incrementing.column.name": "<primary_key_id_column>"**
    - This option specifies the name of the primary key column in the source table that the connector uses to track the order of records.
    - This column is usually an auto-incrementing integer (e.g., id), and it helps the connector identify the most recent records by comparing the values of this column.

 - **"auto.create": "true"**
    - In the sink connector configuration, this setting ensures that if the destination table does not exist in the database, the connector will automatically create it when it starts. 
    - This eliminates the need for manual table creation and ensures seamless integration between the source and destination.

 - **"auto.evolve": "true"**
    - This setting allows the sink connector to automatically adapt to schema changes from the source table. 
    - If columns are added, removed, or modified in the source, these changes will be automatically reflected in the destination table. 
    - It ensures that the destination table's schema remains in sync with the source without requiring manual intervention.

### Flow (Timestamp+Incrementing):

**Source Data (MySql) ---> Kafka Topic ---> Destination Data (MySql)**

- This type of mode is used to capture changes from a relational database in an efficient, incremental manner. 
- It combines two tracking mechanisms:
    - **Timestamp-based tracking**: The connector uses a column with a `timestamp (timestamp.column.name)` to detect records that have been modified or added since the last poll. This allows it to pick up new or updated rows based on the timestamp.
    - **Incremental tracking**: The connector also uses an `incrementing column (usually a primary key, such as id)` to maintain the order of records and ensure that no data is skipped. This column is typically an auto-incrementing integer or a unique value that allows the connector to keep track of the last processed record.

- This mode is ideal for scenarios where you want to capture both updates and new inserts in a database, efficiently syncing the data without reprocessing the entire table.
- Any change of schema in the source database table will automatically gets affected in the destination database table.

### Steps to follow:

1. Make sure you have configured docker properly.

2. **Creating docker-compose file**
    - [Refer this file](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_5/docker-compose.yml) to understand which services I've used for this use case.

3. Start the container will all the services in the docker-compose file.
    - The below command will start the container with all the images as mentioned in the `docker-compose` file.
    ```bash
    docker-compose up -d
    ```
    - **Verify** whether the container has started running (under container tab) by opening the `Docker Desktop Application`.
    OR by using the below command:
    ```bash
    docker ps
    ```
4. Enter `mysql bash cli`, there are multiple ways to do this:
    - You can open the `Docker Desktop Application` and go to `Mysql image` and then go to `Exec` Tab
    OR
    - You can continue to the write commands in the `terminal` window itself.
    - While doing it on the terminal, you have to enable the mysql bash prompt in order to write sql commands.
    - Run `docker exec -it mysql bash`, this will enable mysql bash.

5. **Login into mysql**
    - Run `mysql -u root -p` (replace root with your username you set up in the configuration.)
    - Then it will prompt you to the enter password, type password and then enter.
    - If done correctly, you can now write sql statements.

6. **Create table and insert values into the table**.
    - 1. Create a database if not already created and *use* it. (I used `kafkaa_test` as the *database name*)
            ```sql
            CREATE DATABASE database_name;
            USE database_name;
            ```
    - 2. Create source table.
            ```sql
            CREATE TABLE source_table (
                id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                update_ts TIMESTAMP NOT NULL,
                PRIMARY KEY (id)
            );
            ```
    - 3. Insert some values in the table.
            ```sql
            INSERT INTO source_table (id, name, update_ts) VALUES (1, 'Bryony Smith', '2024-12-18 10:00:00');
            INSERT INTO source_table (id, name, update_ts) VALUES (2, 'Chris Green', '2024-12-18 10:00:00');
            INSERT INTO source_table (id, name, update_ts) VALUES (3, 'Mark Simpson Parker', '2024-12-18 10:00:00');
            ```

7. Create a source connection file `(source_connection.json)` as a **source connector** file. [Refer source_connection file](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_5/source_connection.json)

8. Now, post this file so that kafka will be able to *pull the data from the source mysql table into the kafka topic*.
    ```bash
    curl -X POST -H "Content-Type: application/json" --data @source_connection.json http://localhost:8083/connectors
    ```
    - (Replace the json file name with the file name you configured, i used `source_connection.json`)

9. Check *Control Center* `(http://localhost:9021)` and visit Topics to see the data has been received in the kafka topic or not.

10. (Optional Step) You can also view the topic in the *kafka container*
    - Visit the `kafka bash terminal` by executing the following command in a terminal window.
        ```bash
        docker exec -it <kafka-container-id> /bin/bash
        ```
    - Replace the `<kafka-container-id>` with the id of kafka container, you can get that using `docker ps` command.
    - Then, once you are in kafka bash cli, enter the following command to *list all the topics*:
        ```bash
        /usr/bin/kafka-topics --list --zookeeper zookeeper:2181
        ```

11. (Optional Step) Try to put more records on the source table and see whether those new records are being reflected in the kafka topic.

12. Now, Create a sink connection file `(sink_connection.json)` as a **sink connector file** for receiving the data from the topic to the destinstion mysql table.

13. Now, post the sink json file so that kafka will be able to *pull the data from the kafka topic into the destination mysql table*. [Refer sink_connection file](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_5/sink_connection.json)
    ```bash
    curl -X POST -H "Content-Type: application/json" --data @sink_connection.json http://localhost:8083/connectors
    ```
    - (Replace the json file name with the file name you configured, i used `sink_connection.json`)

14. Login to the mysql bash and check the data into the sink table. (At this point table will be automatically created, we manually dont have to create it.)

15. Lets first update records with updated time stamp
    ```sql
    UPDATE source_table
    SET name = 'B Smith', update_ts = '2024-12-18 10:05:00'
    WHERE id = 1;
    ```
    ```sql
    UPDATE source_table SET name = 'Chris Green', update_ts = '2024-12-17 10:10:00' WHERE id = 2;

    UPDATE source_table SET name = 'M S Parker', update_ts = '2024-12-18 10:15:00' WHERE id = 3;
    ```

16. Verify the records have been updated in both source and sink tables.
![u5_step_16](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/images/u5_step_16.png)

17. **Let's change the source table, add another column**.
    ```sql
    ALTER TABLE source_table 
    ADD Nationality VARCHAR(20);
    ```

18. See the source table now,it should have newly added column *Nationality*.
![u5_step_18](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/images/u5_step_18.png)

19. (Optional) Update a value to check if the records do get updated in both source and sink tables.
    ```sql
    UPDATE source_table 
    SET Nationality = 'ENG' 
    WHERE ID = 1;
    ```
    - Query the source and sink table and you would see the updated records;
    ![u5_step_19](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/images/u5_step_19.png)

**NOTE**: Make sure you have [jars](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/jars) folder present in your working directory

---

### Configurations Used for Connectors:

- ##### Source Connector

| Configuration       | More Information                                                                                   | Description                     |
|---------------------|----------------------------------------------------------------------------------------|---------------------------------|
| name                | [name](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#name)                         | Configuration name              |
| connector.class     | [connector.class](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#connectorclass)     | Class of the connector          |
| tasks.max           | [tasks.max](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#tasksmax)                 | Maximum tasks                   |
| connection.url      | [connection.url](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#connectionurl)       | URL for connection              |
| connection.user     | [connection.user](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#connectionuser)     | User for connection             |
| connection.password | [connection.password](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#connectionpassword) | Password for connection         |
| mode                | [mode](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#mode)                           | Mode of operation               |
| query     | [query](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Concepts/source.md#query)     | Querying to extract columns from the table                  |
| error.tolerance     | [error.tolerance](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#errortolerance)     | Error tolerance level           |
| errors.log.enable   | [errors.log.enable](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#errorslogenable)   | Enable error logging            |
| topic.prefix        | [topic.prefix](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#topicprefix)           | Prefix for topics               |
| poll.interval.ms    | [poll.interval.ms](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/source.md#pollintervalms)    | Poll interval in milliseconds   |

- ##### Sink Connector
| Configuration       | More Information                                                                                   | Description                     |
|---------------------|----------------------------------------------------------------------------------------|---------------------------------|
| name                | [name](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#name)                         | Configuration name              |
| connector.class     | [connector.class](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#connectorclass)     | Class of the connector          |
| tasks.max           | [tasks.max](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#tasksmax)                 | Maximum tasks                   |
| connection.url      | [connection.url](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#connectionurl)       | URL for connection              |
| connection.user     | [connection.user](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#connectionuser)     | User for connection             |
| connection.password | [connection.password](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#connectionpassword) | Password for connection         |
| topics               | [topics](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#topics)                         | Topic name                      |
| insert.mode         | [insert.mode](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#insertmode)             | Insert mode                     |
| auto.create         | [auto.create](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#autocreate)             | Auto create setting             |
| auto.evolve         | [auto.evolve](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#autoevolve)             | Auto evolve setting             |
| batch.size          | [batch.size](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#batchsize)               | Batch size                      |
| max.retries         | [max.retries](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#maxretries)             | Maximum retries                 |
| retry.backoff.ms    | [retry.backoff.ms](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#retrybackoffms)    | Retry backoff in milliseconds   |
| key.ignore          | [key.ignore](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#keyignore)               | Ignore key setting              |
| table.name.format   | [table.name.format](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#tablenameformat)   | Table name format               |
| pk.mode             | [pk.mode](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#pkmode)                     | Primary key mode                |
| pk.fields           | [pk.fields](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Concepts/sink.md#pkfields)                 | Primary key fields              |
