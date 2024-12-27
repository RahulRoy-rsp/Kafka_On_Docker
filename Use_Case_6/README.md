# Spark Streaming with Kafka

This folder shows how we can implement Spark structured Streaming which takes the data from a topic and we use spark to process the data.
And as the data is very nested, it does some level of transformations as well before sending the data into the sink tables, plus into parquet files. We will also be using checkpoint() to make sure no data is processed multiple times. 

### Flow:

**Events are passed using kafka producer ---> Kafka Topic ---> Read Stream ---> Transformation in Spark ---> Write Stream ---> 1. Output folder (parquet format) & 2. Final Table (MySql)**

### Steps to follow:

1. Make sure you have configured docker properly.

2. **Creating docker-compose file**
    - [Refer this file](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_6/docker-compose.yml) to understand which services I've used for this use case.

3. Start the container will all the services in the docker-compose file.
    - The below command will start the container with all the images as mentioned in the `docker-compose` file.
    ```bash
    docker-compose up -d
    ```
    - **Verify** whether the container has started running (under container tab) by opening the `Docker Desktop Application`.
    ![use-case-6_3](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/images/use-case-6_3.png)
    OR by using the below command:
    ```bash
    docker ps
    ```
4. Now access the jupyter-lab environment, by opening the docker app and opening jupter-lab logs
    - you can see the server details as I saw when I started
    ![use-case-6_4](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/images/use-case-6_4.png)
    - visit the last link to open the lab environment which has spark setup.
    - once opened the linked you'll see the interface as follows:![use-case-6_4_2](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/images/use-case-6_4_2.png)

5. Creating files in `jupyter-lab` environment
    1. Create a folder of any name you like, I created `Spark-Stream-with-kafka`
    2. Now, create a python notebook inside that folder, I named it `kafka-mysql-stream.ipynb`. [Refer this file](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_6/kafka-mysql-stream.ipynb)

6. Create kafka topic
    1. You can enter the kafka bash interface by following command:
        ```bash
        docker exec -it <kafka-container-id> bash
        ```
    2. Once you are in kafka bash, let's first list the available topics.
        ```bash
        kafka-topics --list --bootstrap-server <server-link>
        ```
        for me, it was `kafka-topics --list --bootstrap-server localhost:29092` according to my *docker-compose* file
    3. Next, let's create a topic that will be used to consume the data from.
        ```bash
        kafka-topics --create --topic <topic-name> --bootstrap-server <server-link>
        ```
        for me, I created a topic named `player-data`
        ```bash
        kafka-topics --create --topic player-data --bootstrap-server localhost:29092
        ```
    4. *(Optional step)* List the topics again, and now you'll see the topic that you created.

7. **Produce data to kafka topic using kafka producer** 
    1. Open the producer and send messages to the topic.
        ```
        kafka-console-producer --topic <topic-name> --bootstrap-server <server-link>
        ```
        for me, it was as follows, as per my `docker-compose` file 
        ```bash
        kafka-console-producer --topic player-data --bootstrap-server localhost:29092
        ```

8. **Login into mysql and create the sink table**
    - Run `mysql -u root -p` (replace root with your username you set up in the configuration.)
    - Then it will prompt you to the enter password, type password and then enter.
    - If done correctly, you can now write sql statements.
    - Create the database if not exists already and use it.
    - Then, create the sink table
        ```sql
        CREATE TABLE players_raw_table (
            gameID VARCHAR(255),
            player_ID VARCHAR(255),
            player_name VARCHAR(255),
            recorded_at VARCHAR(255)
        );
        ```
9. Run the python notebook

10. Now visit the kafka producer terminal and send in the data.
    1. Paste the sample event from the [Sample-1](https://github.com/RahulRoy-rsp/Kafka_On_Docker/blob/main/Use_Case_6/sample_data/sample1.json)
    2. Check the jupyter-notebook to see if any batch is being updated.
    3. Also, visit mysql terminal and query the table to see if the records are inserted.
    4. Likewise, you can input the other [Sample events](https://github.com/RahulRoy-rsp/Kafka_On_Docker/tree/main/Use_Case_6/sample_data) and verify the data.
