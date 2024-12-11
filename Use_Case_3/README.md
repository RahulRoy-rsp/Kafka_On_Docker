# Change Data Capture (CDC)

This folder explains how you can implement a simple CDC using kafka.

---

### Use Case: 

- We create tables in a database and then inserts a few records into the tables. 
- Then, we will try to catch the changes when there is any updates in the tables.

---

### Steps to Follow:

1. Make sure you have configured docker properly.

2. **Creating docker-compose file**
    - The services that we need for this use-case are *postgres, pgadmin (optional), kafka, zookeeper, debezium, schema-registry.* 
    - `postgres` is the database we will be using for the tables.
    - `pgadmin` is used as web UI for querying the tables.
    - `kafka` is used as the distributed streaming platform.
    - `zookeper` is used for distributed services that helps manage kafka's cluster.
    - `debezium` is used for change data capture, which streams data change from database to kafka.
    - `schema-registry` is used for managing AVRO schemas used by Kafka *Producers* and *Consumers*.
    - [Refer this file](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/docker-compose.yml).

3. Now that you've configured all the services in the `docker-compose` file, it's time to start the container so that all the services will be online. 
    - Run `docker-compose up -d` command in the terminal.
    - The above command will start the container with all the images as mentioned in the `docker-compose` file.
    - Verify whether the container has started running (*under container tab*) by opening the Docker Desktop Application.
    - ![You can see the below output](images/cdc_container_up.png).
    - Alternatively, you can run `docker ps` to see the containers status.

4. Creating source json file
    - Create a json file which will have the configurations related to the postgres. [Refer this](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/debezium_source.json).

5. Now, as all the services are active, **Sign in to PGadmin**.
    - ![Container kaf-pg-cdc](images/cdc-container.png)
    - As you can see the link for pgadmin, visit that page and it will ask you to sign in to the account.
    - ![Sign up pgadmin](images/pgadmin_signup.png)
    - Use the credentials you entered in the [`docker-compose`](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/docker-compose.yml) file.
    - Once signed in, right click on the *Server* and *Register* and then *Server*
    ![register](images/pg_register.png)
    - Enter a unique Server name.
    - Enter the correct *hostname, database name, user and password* as you mentioned in the [`docker-compose`](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/docker-compose.yml) file.

6. **Create Tables**
    - Select the database you mentioned and visit query editor.
    - Create the three tables that we will be using for this use case, we will only track CDC on two tables. (Of course, I could have added many more columns to each respective tables) [Refer this for SQL](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/queries.sql).

7. **Add logical replication to the tables**
    - In systems like *Debezium*, which uses logical replication to capture changes in a PostgreSQL database, **REPLICA IDENTITY FULL** ensures that the entire row is logged, making it possible to capture both the before and after images of a row during updates. This allows Debezium to stream data changes accurately.
    - Without **REPLICA IDENTITY FULL**, only primary key columns (if present) would be replicated, which might not be enough to identify rows when there are updates or deletes without primary keys.
    [Refer this for SQL](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/queries.sql).

8. Connecting kafka and postgres.
    - The curl command is used to send an HTTP POST request to create a new connector in **Kafka Connect**. 
    - **Kafka Connect** is a tool for scalable and fault-tolerant data integration between Kafka and external systems, like databases, file systems, or other messaging systems. 
    - In this case, we're interacting with the Debezium connector, which is used for **Change Data Capture (CDC)**.
    - General syntax: 
        ```bash
        curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" link_of_the_connectors --data @the_source_json_file
        ```
    - So for our case, run the following command: 
        ```bash
        curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ --data @debezium_source.json
        ```
    - To verify, run the command `curl localhost:8083/connectors/`, it will list down the connectors.

9. Now, insert some values in the tables. [Refer this for SQL](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/queries.sql).

10. Verify with the select statements on the tables to view the data.

11. Run `kafkacat` to consume messages (I recommend typing commands for all three tables in three different command prompts, this will help you see the output more precisely).
    - General Syntax:
        ```bash
        docker run --tty --network *you-folder-name-followed-by-default* confluentinc/cp-kafkacat kafkacat -b kafka:9092 -C -s key=avro -s value=avro -r *schema-registry-link* -t *table-name-for-cdc*
        ```
    - For `player_history`
        ```bash
        docker run --tty --network kaf-pg-cdc_default confluentinc/cp-kafkacat kafkacat -b kafka:9092 -C -s key=avro -s value=avro -r http://schema-registry:8081 -t postgres.public.player_history
        ```
    - For `goal_history`
        ```bash
        docker run --tty --network kaf-pg-cdc_default confluentinc/cp-kafkacat kafkacat -b kafka:9092 -C -s key=avro -s value=avro -r http://schema-registry:8081 -t postgres.public.goal_history
        ```
    - For `points_table`
        ```bash
        docker run --tty --network kaf-pg-cdc_default confluentinc/cp-kafkacat kafkacat -b kafka:9092 -C -s key=avro -s value=avro -r http://schema-registry:8081 -t postgres.public.points_table
        ```
12. Now, insert some more records in the tables. [Refer this for SQL](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/queries.sql).

13. See the output for the three tables.
    - For `player_history`
    ![player_history-1](images/player_history-1.png)

    - For `goal_history`
    ![goal_history-1](images/goal_history-1.png)

    - For `points_table` (No update to see, because CDC was not set for this table)
    ![points_table-1](images/points_table-1.png)

14. Now, lets update records in the tables wherein CDC is active. [Refer this for SQL](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_3/queries.sql).

15. See the updated output for the two tables.
    - For `player_history`
    ![player_history-2](images/player_history-2.png)

    - For `goal_history`
    ![goal_history-2](images/goal_history-2.png)