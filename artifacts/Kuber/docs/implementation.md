---
layout: default
title: Implementation
nav_order: 2
has_children: false
permalink: /docs/Implementation
---

## The source code of our framework is available on [GitHub](https://github.com/kubercostoptimizer/Kuber/tree/master/code).
## Docker container with all the dependencies is at [Docker Hub](https://hub.docker.com/r/kuberload/kuber)
---

## Prerequisites for Running
1. A working OpenNebula Cluster: for creating VMs. Installation instructions are available [here](https://docs.opennebula.io/5.12/deployment/index.html).  
2. A [DockerHub](https://hub.docker.com/) account: stores apps’ Docker images for Kubernetes to deploy.

---
## Code Structure
The code is found in [Github](https://github.com/kubercostoptimizer/Kuber/tree/master/code) and is arranged in the following packages:
1. [Infrastructure](https://github.com/kubercostoptimizer/Kuber/tree/master/code/Infrastructure): handles low-level functions
    - Uses OpenNebula API to creates VMs of required type. 
    - Deploys Kubernetes on to VMs or adds new VM. 
    - Deploys combinations using Kubernetes API.
2. [Profiler](https://github.com/kubercostoptimizer/Kuber/tree/master/code/Profiler): Executes a combination on a VM type
    - Creates initial cluster needed for all services in the app.
    - Uses the Infrastructure package to place the service combination on the test VM.
    - Loads the databases for the app.
    - Loads tests of the app and extracts performance data from the Istio logs. 
3. [Kuber](https://github.com/kubercostoptimizer/Kuber/tree/master/code/kuber): code of the Combination Selector and Deployment Planner components.
4. [SSOT](https://github.com/kubercostoptimizer/Kuber/tree/master/code/SSOT): Configuration information about VM types and services.
5. [Apps](https://github.com/kubercostoptimizer/Kuber/tree/master/code/apps): Application deployment files and load tests.

---
## Configuration

Kuber needs the following information to be provided by the application developer:

### Data about the application

1. Kubernetes deployment files (.yamls) for deploying services and their dependencies.
   - place all the deployment files in /apps/app_name/deploy folder.
2. Load test to execute.
   - copy existing load_test folder from /apps/sock-shop/load_test
   - update /apps/app_name/load_test/locustfile.py with required test scenario.
3. Initial load, e.g., for databases
   - create a folder apps/app_name/load_test/init_scripts/
   - Copy the code the initializes the application.
   - Create a file run.sh and modify the file to invoke the code from it.
   - Example: if initialization script is a python code init.py, add a line to run.sh:
   ```python
       python init.py
   ```

### SSOT: Single Source Of Truth

Application developers have to configure VM types and services that need to be tested in file SSOT/config.json. 
Example config.json file is in the SSOT folder. 
Below we explain in detail each of the config options:

``` json
{
  "Application": 
      {
          "name": "app_name",
          "services": ["service1", "service2"],
          "front-end": "service1",
          "port": "5000"
      },
  "Profiling":
      {
        "load_gen":
          {
           "time_limit":"2m",
           "concurrent":"100"
          }
      },
  "Infrastructure":
      {
        "Cloud_provider": "opennebula",
        "vm_types":[
                {
                  "name"          : "m4.large",
                  "cpu_count"     : "2",
                  "ram"           : "8",
                  "computer"      : "leibnitz",
                  "price"         : 0.10
                },
                {
                  "name"          : "m4.xlarge",
                  "cpu_count"     : "4",
                  "ram"           : "16",
                  "computer"      : "leibnitz",
                  "price"         : 0.20
                },
              ]
      }
}
```
1.	Application
    - name: the name of the application (should be same as the namespace given in Kubernetes deployment files and the folder name in /apps).
    - services: names of each microservice, should be the same as in the Kubernetes services in /apps/app_name/deploy.
    - front-end: service that receives external traffic for the application.
    - port: port exposed by front-end.
2.	Profiling
    - time_limit: the amount of time to run each load test.
    - concurrent: number of concurrent users for the test.
3.	VM types: a list where each entry corresponds to a VM type and contains
    - name: user-given name for the VM type
    - cpu_count: number of CPU cores
    - ram: RAM size in GB
    - price: cost per hour in $
    - computer: a physical machine to place the VM on, i.e., a hostname in OpenNebula cluster.

   
---
## Running the Kuber with Docker container
 - Download the docker container from the [DockerHub](https://hub.docker.com/r/kuberload/kuber) and the code from [GitHub ](https://github.com/kubercostoptimizer/Kuber/tree/master/code).
 - Run the docker container with code using the following command:
        
```sh
docker run -it -v /code:/wd/code kuberload/kuber:latest /bin/bash
```
        
 - Update login credentials for OpenNebula Cluster and DockerHub
        
```sh
#OpenNebula Cluster Credentials
export USERNAME= xxxx #OpenNebula username
export PASSWORD= xxxxx #OpenNebula password
export USERID= xxxx #OpenNebula userid

#DockerHub Credentials
export DOCKERID= xxxx #DockerHub username
export DOCKERPASS= xxxx #DockerHub password
export DOCKERMAIL= xxxx #DockerHub mail
```
        
 - Finally, execute the Kuber inside the container:
        
```sh
cd /wd/code/kuber
python run.py
```
