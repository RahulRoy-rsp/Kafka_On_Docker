# Docker Swarm

- Docker Swarm is a native clustering and orchestration tool for Docker. 
- It enables you to manage a cluster of Docker nodes (servers) as a single virtual system, simplifying the deployment, scaling, and management of containerized applications.

### Key Concepts

1. **Node**: A node is an individual Docker engine participating in the Swarm. There are two types of nodes:
   - **Manager Node**: Responsible for managing the Swarm and orchestrating tasks.
   - **Worker Node**: Executes tasks assigned by the Manager.

2. **Service**: A service is the definition of a task to be executed. It specifies the Docker image to use, the number of replicas, and other configurations.

3. **Task**: A task is a unit of work assigned to a node. Each service consists of multiple tasks.

4. **Cluster**: A group of nodes working together as a single system.

---

Here’s a basic guide to getting started with Docker Swarm:

#### Step 1: Initialize Docker Swarm

To initialize a Docker Swarm, run the following command on the node you want to designate as the Manager:

```bash
docker swarm init
```

This command will output a join token that you can use to add worker nodes to the Swarm.

#### Step 2: Add Worker Nodes to the Swarm

On the other nodes (workers), run the following command using the join token provided by the Manager node:

```bash
docker swarm join --token <SWARM_JOIN_TOKEN> <MANAGER_IP>:2377
```

Replace `<SWARM_JOIN_TOKEN>` with the token provided by the Manager and `<MANAGER_IP>` with the IP address of the Manager node.

#### Step 3: Deploy a Service

Once the nodes are part of the Swarm, you can deploy services. For example, to deploy an NGINX service with 3 replicas, use the following command:

```bash
docker service create --name my_nginx --replicas 3 -p 80:80 nginx
```

#### Step 4: Manage the Swarm

You can manage and monitor the Swarm using various commands:

- **List Nodes**:
  ```bash
  docker node ls
  ```
  This command lists all the nodes in the Swarm, showing their roles and statuses.

- **List Services**:
  ```bash
  docker service ls
  ```
  This command lists all the services running in the Swarm.

- **Inspect Service**:
  ```bash
  docker service inspect my_nginx
  ```
  This command provides detailed information about a specific service.

- **Scale Service**:
  ```bash
  docker service scale my_nginx=5
  ```
  This command scales the service to 5 replicas.

- **Remove Service**:
  ```bash
  docker service rm my_nginx
  ```
  This command removes the specified service from the Swarm.

### Example Workflow

1. **Initialize Swarm** on the Manager node:
   ```bash
   docker swarm init
   ```

2. **Join Worker Nodes** to the Swarm using the token provided:
   ```bash
   docker swarm join --token <SWARM_JOIN_TOKEN> <MANAGER_IP>:2377
   ```

3. **Deploy a Service**:
   ```bash
   docker service create --name my_nginx --replicas 3 -p 80:80 nginx
   ```

4. **Scale the Service**:
   ```bash
   docker service scale my_nginx=5
   ```

5. **List Services**:
   ```bash
   docker service ls
   ```

6. **Remove the Service**:
   ```bash
   docker service rm my_nginx
   ```

Docker Swarm makes it easy to deploy, manage, and scale applications across multiple Docker nodes, providing high availability and fault tolerance.
