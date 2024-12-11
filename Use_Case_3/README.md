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
