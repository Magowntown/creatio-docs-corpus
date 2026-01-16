<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/containerized-components/machine-learning-service)** (8.3).

Version: 8.2All Creatio products

On this page

Machine learning service predicts values based on large volumes of historical data and current facts. Learn more in a separate article: [Predictive data analysis](https://academy.creatio.com/documents?id=1825).

Important

Base knowledge of Docker, Linux or Windows administration is required to set up the machine learning service.

## Getting started [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-1 "Direct link to Getting started")

Note. Creatio on-site requires the "creatio predictive service on-site" [license](https://academy.creatio.com/documents?id=1264) for the service to operate as intended. If you need to purchase the license, contact the responsible manager.

To set up the service, you need to have a server (physical or virtual machine) with Linux or Windows OS installed. Docker software is used for installing the service components. Download the archive containing the configuration files and installation scripts. [Download archive](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/downloads/machine_learning/ml_docker-compose_4.0.103_2024_12_20.zip). Depending on your company needs, you can use either Docker Community Edition (CE) or Enterprise Edition (EE). Learn more in the [Docker Guide](https://docs.docker.com/install/overview/).

Attention. We recommend using a Linux-based server for production environment. You can only use a Windows based server for the development environment. Contact the support service to receive Docker containers that care compatible with Windows.

Use the [requirements calculator](https://academy.creatio.com/docs/requirements/calculator) to check the server requirements.

## Machine learning service components [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-4 "Direct link to Machine learning service components")

The machine learning service uses the following components (Fig. 1):

- **ML Service**. Machine learning web service. The only component enabling external access.

- **Python Engine**. Machine learning wrapper service for open-source machine learning libraries.

- **ML Task Scheduler**. Task scheduler.

- **MySQL**. MySQL database. You can access it via the standard 3306 port.


Fig. 1 Machine learning service components

![Fig. 1 Machine learning service components](https://academy.creatio.com/sites/default/files/pictures/SchemyBezOU_EN/BezOU+ML.png)

All the components are packed as Docker images for the convenient on-site installation of the service.

## Set up machine learning service [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-5 "Direct link to Set up machine learning service")

Follow this procedure to set up the machine learning service:

1. Install Docker. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-6)

2. Install Docker Compose. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-7)

3. Install and set up the service components. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-8)

4. Verify the installation. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-10)


### Install Docker [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-6 "Direct link to Install Docker")

Docker installation on Linux platforms is covered in the [Docker guide](https://docs.docker.com/install/).

Run the "docker --version" command on Linux machine to verify the installed Docker version.

### Install Docker Compose [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-7 "Direct link to Install Docker Compose")

Docker Compose installation on Linux platforms is covered in the [Docker guide](https://docs.docker.com/install/).

Run the "docker-compose --version" command on Linux machine to verify the installed Docker Compose version.

### Set up the machine learning service components [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-8 "Direct link to Set up the machine learning service components")

Deploy the containers of the machine learning service components via the Docker Compose utility. Download the configuration files and scripts that are necessary to deploy and configure the service components. [Download the archive](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/downloads/machine_learning/ml_docker-compose_4.0.103_2024_12_20.zip)

Note. The configuration files contain all necessary default settings for a Linux based server.

The **archive structure of the configuration files and scripts** is as follows:

**/etc/**

**../ml-service/appsettings.json**. The ML web service configuration.

**../ml-service/log4net.config**. The setup of the web service logging level.

**../task-scheduler/appsettings.json**. The "ML Task Scheduler" utility configuration.

**../task-scheduler/log4net.config**. The setup of "ML Task Scheduler" logging level.

**Docker-compose.yml**. The "Docker Compose" utility configuration.

**.env**. The file that contains environment variables for running the components. For example, MySQL password.

Attention. If you need to change the password to MySQL database, update it in the .env file and other configuration files that contain database access setup sections.

#### Install the machine learning service components [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-9 "Direct link to Install the machine learning service components")

1. Download and unzip the archive with the configuration files and scripts to a custom directory, for example, /opt/ml.

2. Using the Linux terminal, go to the /docker-compose catalog of the unzipped archive, for example, /opt/ml/docker-compose.

3. Run the "sudo docker-compose pull" command in the terminal. Wait until the download of the required service component images from the [Docker Hub](https://hub.docker.com/) is complete.

Attention. If the server is disconnected from the Internet, download all required images to an Internet-connected computer manually (see the "docker-compose.yml" configuration file). Then use the [sudo docker export](https://docs.docker.com/engine/reference/commandline/export/) and [sudo docker import](https://docs.docker.com/engine/reference/commandline/import/) commands to transfer the images to the target computer as files.

4. Run the **sudo docker-compose run dbmigration** command to initialize the database structure. Wait until the command execution is complete.

5. Run the **sudo docker-compose up -d** command to launch the services. A "logs" folder will be created in the current catalog.


### Verify the setup of the machine learning service components [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-10 "Direct link to Verify the setup of the machine learning service components")

1. To verify the installation of ML web service, run the following command in Linux:

**curl -X GET localhost:5005/readiness**

The service must return the following response:

**Healthy**

2. To verify the running of ML Task Scheduler, execute the following command in the Linux terminal:

**curl -X GET localhost:5004/readiness**

The service must return the following response:

**Healthy**

3. To verify the running of R Engine, execute the following command in the Linux terminal:

**curl -X GET localhost:8081/readiness**

The service must return the following response:

**R Service is ready**

4. To verify creating of tables, run the following command in the terminal:

**docker exec -it DB Container Id mysql -u root --password=Supervisor ml -e "show tables;"**

where DB Container Id is an identifier of the container with a database component. You can find out the container identifier using the **sudo docker ps** command.

Example. Verification of creating tables:

docker exec -it DB Container Id mysql -u root --password=Supervisor ml -e "show tables;"

As a result, the names of primary service tables should be displayed: "modelinstance", "traindata", "trainsession", etc.


### Perform the setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-23 "Direct link to Perform the setup in Creatio")

To work with the prediction service in Creatio, fill out the following settings:

1. "Creatio cloud services API key" ("CloudServicesAPIKey" code) system setting. Cloud services need it to authenticate your Creatio instance.  For Creatio instances deployed on-site set this setting to value `*`.
2. "Periodicity of machine learning model training job" ("MLModelTrainingPeriodMinutes" code) system setting. It determines the models' synchronization launch frequency.
3. Add the prediction service's URL to the Service endpoint Url field for all the records in the ML problem types lookup.

## Update the machine learning service components [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#title-257-11 "Direct link to Update the machine learning service components")

Attention. We recommend saving a backup copy of MySQL database, before you update the services. Learn more in the [Docker Guide](https://dev.mysql.com/doc/refman/8.0/en/backup-and-recovery.html).

1. Using the Linux terminal, go to the docker-compose catalog with the configured files, for example, /opt/ml/docker-compose.

2. Run the **sudo docker-compose stop** command to stop the service component containers.

3. Run the **sudo docker-compose pull** command in the terminal. Wait until the download of the required service component images from the [Docker Hub](https://hub.docker.com/) is complete.

4. Run the **sudo docker-compose run dbmigration** command to initialize the database structure. Wait until the command execution is complete.

5. Run the **sudo docker-compose up -d** command to launch the services.

Attention. If your application already has configured and trained data models, we recommend retraining them after updating the service.


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service\#see-also "Direct link to See also")

[Predictive analysis](https://academy.creatio.com/documents?id=1825)

[Machine learning service (development guide)](https://academy.creatio.com/documents?id=15067)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [Getting started](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-1)
- [Machine learning service components](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-4)
- [Set up machine learning service](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-5)
  - [Install Docker](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-6)
  - [Install Docker Compose](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-7)
  - [Set up the machine learning service components](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-8)
  - [Verify the setup of the machine learning service components](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-10)
  - [Perform the setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-23)
- [Update the machine learning service components](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#title-257-11)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/containerized-components/machine-learning-service#see-also)