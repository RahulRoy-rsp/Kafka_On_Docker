# Simple Bulk Transfer

This folder explains how you can implement a bulk transfer from a MySql database to MySql Database.

### Flow (Bulk Transfer):
**Source Data (MySql) ---> Kafka Topic ---> Destination Data (MySql)**

---
### Use-Case:

- For this use-case I had a very simple example wherein I wanted to have a source table which consists of columns like id, name and role.
- All I wanted to do was to write some data into the source table and that data should be extracted to the Kafka Topic regularly which means pull the whole data in the Topic and then in the final destination table i'll be pulling the data from the topic.

### Steps to follow:

1. Make sure you have configured docker properly.

2. **Creating docker-compose file**
  - [Refer this file](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_1/docker-compoese.yml) to understand which services I've used for this use case.

3. Now, that you've configured everything that we need for this use-case, it's time to start the container.
  - Run `docker-compose up -d` command in the terminal.
  - The Above command will start the container with all the images as mentioned in the `docker-compose` file.
  - Verify whether the container has started running (*under container tab*) by opening the Docker Desktop Application.

4. As all the services has started, it's time to configure the tables in the mysql database.

5. There are multiple ways to do this:
  - You can open the Docker Desktop Application and go to Mysql image and then go to Exec Tab
  OR
  - You can continue to the write commands in the terminal window itself.
  - While doing it on the terminal, you have to enable the mysql bash prompt in order to write sql commands.
  - Run `docker exec -it mysql bash`, this will enable mysql bash.

6. Login into mysql
  - Run `mysql -u root -p` (replace root with your username you set up in the configuration.)
  - Then it will prompt you to the enter password, type password and then enter.
  - If done correctly, you can now write sql statements.

7. Create table and insert values into the table.

  - Create a database if not already created and use it.

  - **Creating Source Table**
  ```sql
  CREATE TABLE source_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR (20)
  );
  ```

  - **Inserting Values**
  ```sql
  INSERT INTO source_table (name) VALUES ('Kacy');
  INSERT INTO source_table (name) VALUES ('Ricky');
  ```

  - Query the table to see whether the records has been inserted.

  - Once done, you can exit mysql using `exit` command.

8. Create a source connection file `(source_connection.json)` as a source connector file.
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

9. Now, post this file so that kafka will be able to pull the data from the source mysql table into the kafka topic.

  - `curl -X POST -H "Content-Type: application/json" --data @source_connection.json http://localhost:8083/connectors` (Replace the json file name with the file name you configured)

10. Check *Control Center* `(http://localhost:9021)` and visit Topics to see the data has been received in the kafka topic or not.

11. (Optional Step) Try to put more records on the source table and see whether those new records are being reflected in the kafka topic.

12. Now, Create a sink connection file `(sink_connection.json)` as a sink connector file for receiving the data from the topic to the destinstion mysql table.
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

13. Create desination table, follow the same steps to enter mysql prompt.
  - **Creating Sink Table**
  ```sql
  CREATE TABLE sink_table (
    id INT PRIMARY KEY,
    name VARCHAR (20)
  );
  ```

14. Now, post the sink json file so that kafka will be able to pull the data from the kafka topic into the destination mysql table.

  - `curl -X POST -H "Content-Type: application/json" --data @sink_connection.json http://localhost:8083/connectors` (Replace the json file name with the file name you configured)

15. Login to the mysql prompt and check the data into the sink table.