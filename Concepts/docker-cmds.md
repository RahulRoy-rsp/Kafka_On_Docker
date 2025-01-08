### Docker Commands
Here are some docker commands every one should know

---
1. **docker --version**
   - **Description**: Returns the installed Docker version.
   - **Usage**: 
     ```bash
     docker --version
     ```
    - It will output the installed docker version. (Eg: `Docker version 27.3.1, build ce12230`)
---
2. **docker pull**
   - **Description**: Downloads a Docker image from a registry (like Docker Hub).
   - **Usage**: 
     ```bash
     docker pull <image_name>
     ```
    - **Example**: Below command will pull the `MySQL image version 8.0` from the `Docker Hub registry` into your local system.
        ```bash
        docker pull mysql:8.0
        ```
---
3. **docker build**
   - **Description**: Builds an image from a Dockerfile.
   - **Usage**: 
     ```bash
     docker build -t <image_name>:tag .
     ```
    - **Example**: Below command builds a `Docker image` named `my_app_image` with the `tag 1.0` from the `Dockerfile` in the current directory.
        ```bash
        docker build -t my_app_image:1.0
        ```
---
4. **docker run**
   - **Description**: Runs a container from an image.
   - **Usage**: 
     ```bash
     docker run -d --name <container_name> <image_name>
     ```
    - **Example**: Below command runs a container named my_app_container from the image my_app_image:1.0 in detached mode.
        ```bash
        docker run -d --name my_app_container my_app_image:1.0
        ```

   - **Flags**:
     - `-d`: Runs the container in detached mode (in the background).
     - `-it`: Runs the container in interactive mode with a terminal.
     - `-p`: Maps a port on the host to a port in the container.
     - `--name`: Assigns a name to the container.
---
5. **docker ps**
   - **Description**: Lists all running containers.
   - **Usage**: 
     ```bash
     docker ps
     ```
---
6. **docker ps -a**
   - **Description**: Lists all containers, including stopped ones.
   - **Usage**: 
     ```bash
     docker ps -a
     ```
---
7. **docker stop**
   - **Description**: Stops a running container.
   - **Usage**: 
     ```bash
     docker stop <container_name>
     ```
    - **Example**: Below command bcommand stops the running container named my_app_container.
        ```bash
        docker stop my_app_container
        ```     
---
8. **docker start**
   - **Description**: Starts a stopped container.
   - **Usage**: 
     ```bash
     docker start <container_name>
     ```
---
9. **docker rm**
   - **Description**: Removes a container.
   - **Usage**: 
     ```bash
     docker rm <container_name>
     ```
    - **Example**: Below command removes container named my_app_container.
        ```bash
        docker rm my_app_container
        ```
---
10. **docker rmi**
    - **Description**: Removes an image.
    - **Usage**: 
      ```bash
      docker rmi <image_name>
      ```
    - **Example**: Below command removes the images of MySql of version 8.0 from the System.
        ```bash
        docker rmi mysql:8.0
        ```
---
11. **docker logs**
    - **Description**: Retrieves logs from a container.
    - **Usage**: 
      ```bash
      docker logs <container_name>
      ```
---
12. **docker exec**
    - **Description**: Runs a command in a running container.
    - **Usage**: 
      ```bash
      docker exec -it <container_name> <command>
      ```
    - **Example**: Below command will enter the mysql cli for writing SQL statements.
        ```bash
        docker exec -it mysql bash
        ```   
---
13. **docker images**
    - **Description**: Lists all images.
    - **Usage**: 
      ```bash
      docker <images>
      ```
---
14. **docker volume**
    - **Description**: Manages Docker volumes.
    - **Usage**:
      ```bash
      docker volume create <volume_name>
      docker volume ls
      docker volume rm <volume_name>
      ```
---
