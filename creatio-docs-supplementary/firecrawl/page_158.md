<!-- Source: page_158 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

The Email Listener (formerly Exchange Listener) service synchronizes Creatio with [Microsoft Exchange](https://academy.creatio.com/documents?id=1418) and [IMAP/SMTP](https://academy.creatio.com/documents?id=1415) mail services using a subscription mechanism. Email Listener lets you use horizontal scaling that enables the active use of email synchronization block and controlled use of resources.

The synchronization service is required to manage emails in Creatio .NET Framework and .NET Core since version 7.17.2 and .NET 6 since version 8.0.8. This article covers the deployment of Exchange Listener synchronization service for Creatio on-site.

The service consists of the following components:

1. **Email Listener (EL API)**. Initiates an outgoing connection to EWS API or IMAP. Creates a subscription to "new message" events using the mailbox credentials. The open subscription remains in the component memory to ensure fast response time when new emails arrive. The email is downloaded upon receiving the corresponding event. An in-memory repository is sufficient to deploy the service. A required service component.
2. **NoSQL Redis DBMS**. Creates a scalable and fault tolerant system of handler nodes. The Redis repository holds information about the mailboxes that are served. This enables any container to handle Creatio requests to add a new subscription or check the status of a specific subscription regardless of the subscription node. Redis requires a separate database for the Exchange Listener service operation. A required service component.
3. **Email Worker (EL Worker)**. Maintains the scalability and fault tolerance of the primary Email Listener module. The additional module downloads emails from the mail server and delivers them to Creatio. This enables high-load services to handle emails smoother during peaks in the email flow. The EL Worker reduces the load on the EL API components that no longer need to download emails. Instead, the components can manage the subscription and send outgoing emails.
4. **RabbitMQ**. Maintains the scalability and fault tolerance of the service. The queue broker distributes tasks between components in high-load environments.

## Determine the configuration of the Email Listener service [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#title-2111-7 "Direct link to Determine the configuration of the Email Listener service")

Determine the configuration of the Email Listener service for your Creatio instance based on the average flow of emails (both incoming and outgoing) that the company mailboxes handle per second.

For example, if your company uses a single support mailbox whose email flow is 4, the recommended configuration includes 15 EL Worker replicas, 4 EL API replicas, and RabbitMQ service.

![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/exchange_listener/scr_exchange_listener_table_system_requirements.png)

note

The number of active EL Worker replicas directly affects the email handling speed. The email flow in production fluctuates, therefore certain EL Worker replicas might stand idle for some time. The article provides recommended configuration parameters, but you can use fewer replicas than the table specifies. In this case, the service will take longer to handle the emails during peak load. Optimize the ratio between the email handling speed and the number of resources utilized according to business requirements.

### Component replica system requirements [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#title-2111-8 "Direct link to Component replica system requirements")

| Component | vCPU | RAM |
| --- | --- | --- |
| EL Worker | 0.1 | 1.1 GB |
| EL API | 0.150 | 850 MB |
| Redis | 0.5 | 3 GB |
| Rabbit MQ | 0.5 | 4 GB |

note

The values in the table are recommended, the actual resource consumption might vary by the service use case. We recommend monitoring the CPU and memory resources on the deployed services to optimize the available limits.

## Email Listener deployment methods [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#title-2111-1 "Direct link to Email Listener deployment methods")

We recommend **using the Kubernetes orchestrator and Helm package manager** to deploy the service. [Read more >>>](https://academy.creatio.com/documents?id=2074&anchor=title-2111-2)

You can also **use Docker** to speed up the deployment in the development environment. [Read more >>>](https://academy.creatio.com/documents?id=2074&anchor=title-2111-4)

### Deploy the synchronization service via Kubernetes [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#title-2111-2 "Direct link to Deploy the synchronization service via Kubernetes")

Deploy the synchronization service using the RabbitMQ programmable message broker.

Take the following steps to deploy the service:

1. Set up the target environment:
1. **Kubernetes cluster**. Learn more about setting up and managing the cluster in the [Kubernetes documentation](https://kubernetes.io/docs/home/).
2. **Helm package manager**. Learn more about installing the package manager in the [Helm documentation](https://helm.sh/docs/intro/install/).
2. **Install Redis**. Redis can be installed as a Kubernetes service or as a standalone service, provided Email Listener pods have access to it. Learn more about installing and using Redis on the [official website](https://redis.io/).

3. **Install the RabbitMQ queue broker**. RabbitMQ can be installed as a Kubernetes service or as a standalone service. Alternatively, you can use any AMQP provider, provided Email Listener pods have access to it. Learn more about RabbitMQ deployment options in the [official documentation](https://www.rabbitmq.com/docs/download).

After the RabbitMQ service is deployed, create a virtual host and Email Listener user in the installed RabbitMQ instance (learn more about accessing remote RabbitMQ server nodes in "Using CLI Tools against Remote Server Nodes").

Create a virtual host and Email Listener user in the installed RabbitMQ instance:
1. Connect to RabbitMQ and run the following command:





      ```cli
      kubectl exec test-rabbit-rabbitmq-0 -n exchange-listener --stdin --tty shell-demo -- /bin/bash
      ```

2. Create a virtual host:





      ```cli
      rabbitmqctl add_vhost ExchangeListener
      ```

3. Create a user and specify the password. Avoid using the "@" character in the password as this can affect the Rabbit MQ connection mechanism.





      ```cli
      rabbitmqctl add_user creatio
      ```

4. Set up the user permissions to the virtual host:





      ```cli
      rabbitmqctl set_permissions --vhost ExchangeListener creatio ".*" ".*" ".*"
      ```
4. **Install the Email Listener module**. To install the module, request the helm package from [Creatio support](mailto:support@creatio.com). View the available parameters of the helm package in the table below.



Important





You need **repository access** to set up the current version of the Email Listener service. Contact [Creatio support](mailto:support@creatio.com) to verify your license and gain access to the repository.



For newer **Kubernetes versions**, specify the API version by adding the following parameter: `--set apiVersion=apps/v1`







Example of a command that uses the address and relative path





```cli
helm upgrade -i
   --set ingress.enabled=true
   --set ingress.path=<listener_path>
   --set ApiUrl=kubernetes
   --set apiVersion=apps/v1
   --set-string Redis.Connection="<redis_host>\,password=<password>"
   --namespace <namespace_name>
   --set WorkerReplicaCount=2
   --set ReplicaCount=2
   --set RabbitMQ.ExchangeName=NewExchange;
   --set RabbitMQ.QueueName=NewQueue;
   --set RabbitMQ.Host=test-rabbit-rabbitmq;
   --set RabbitMQ.HostApi=test-rabbit-rabbitmq;
   --set RabbitMQ.HttpPort=15672;
   --set RabbitMQ.AmqpPort=5672;
   --set RabbitMQ.VirtualHost=ExchangeListener;
   --set RabbitMQ.Login=creatio;
   --set RabbitMQ.Password=creatio; exchangelistener ./home/creatio/exchangelistener-1.0.17.tgz
   --set service.type=NodePort
   --set service.nodePort=port
```





Where:

**<redis\_host>** is the Redis server address.

**<password>** is the Redis password.

**<listener\_path>** is the relative service path for the Email Listener.

**<namespace\_name>** is the Kubernetes namespace where the service will be deployed.

**ReplicaCount** is the number of EL API replicas based on the number of mailboxes and average email flow for your company. View the calculation table above.

**WorkerReplicaCount** is the number of EL Worker replicas based on the number of mailboxes and average email flow for your company. View the calculation table above.

To set up an HTTPS connection, deploy the service with [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) and a valid SSL certificate, as well as specify HTTPS in the `<kubernetes_url>` Email Listener service address, where **<kubernetes\_url>** is your Kubernetes cluster's external domain or IP address.

To check the service availability, send a GET request to the `/api/listeners/status` endpoint (Fig. 1). For example, if using ingress with a path:





```cli
<kubernetes_url>/<listener_path>/api/listeners/status
```







Example of a command that uses Node IP and port address





```cli
helm upgrade -i exchangelistener ./home/creatio/exchangelistener-1.0.17.tgz --namespace default -set ApiUrl=kubernetes --set apiVersion=apps/v1 --set-string Redis.Connection="redis\,password=test" --set WorkerReplicaCount=2 --set ReplicaCount=2 --set RabbitMQ.ExchangeName=NewExchange --set RabbitMQ.QueueName=NewQueue --set RabbitMQ.Host=test-rabbit-rabbitmq --set RabbitMQ.HostApi=test-rabbit-rabbitmq --set RabbitMQ.HttpPort=15672 --set RabbitMQ.AmqpPort=5672 --set RabbitMQ.VirtualHost=ExchangeListener --set RabbitMQ.Login=creatio --set RabbitMQ.Password= creatio --set service.type=NodePort --set service.nodePort=31318
```




Fig. 1 Email Listener service response

![Fig. 1 Email Listener service response](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/exchange_listener/chapter_exchange_listener_answer.png)


Available parameters of the Email Listener helm package



| Parameter | Parameter description | Default value |
| --- | --- | --- |
| replicaCount | Number of StatefulSet handlers. | 2 |
| service.type | Service type. Learn more about the Kubernetes service types in the [Kubernetes documentation](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types). | ClusterIP |
| service.nodePort | If the service.type parameter equals NodePort, specify the external service port in this parameter. Learn more about the NodePort type in the [Kubernetes documentation](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport). |  |
| env.host | Host address for Redis. |  |
| env.port | Host port for Redis. | 6379 |
| env.base | Database number for Redis. |  |
| ingress.enabled | Use address overriding via ingress. | false |
| ApiUrl | Service address if ingress.enabled=true |  |
| ingress.path | Relative service path. |  |
| log4Net.level | Default logging level. | Info |


Use the [system requirements calculator](https://academy.creatio.com/docs/requirements/calculator) to check the server requirements.


### Deploy the synchronization service in Docker [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#title-2111-4 "Direct link to Deploy the synchronization service in Docker")

To set up the service, use a server (computer or virtual machine) that has Linux or Windows OS installed.

Important

We recommend deploying the synchronization service in Docker only to the development environment. This method provides a high deployment speed, but does not enable compliance with the requirements of the product environment, namely: function fault tolerance, scaling for the handling of large request volumes, and a unified approach to component management that uses the container orchestration. For the product environment, we strongly recommend using the Kubernetes orchestrator and Helm package manager.

You need **repository access** to set up the current version of the Email Listener service. Contact [Creatio support](https://academy.creatio.commailto:support@creatio.com/) to verify your license and gain access to the repository.

Take the following steps to deploy the service:

1. Set up the Docker container platform first.

To install Docker Desktop on Windows Server, follow [special instructions](https://docs.microsoft.com/en-us/virtualization/windowscontainers/quick-start/set-up-environment?tabs=Windows-Server) on Microsoft website.

To install Docker on Linux, follow the guide in the [Docker documentation](https://docs.docker.com/install/linux/docker-ce/debian/). To check the installed Docker version, run the following command:





```cli
docker --version.
```





You can install Docker components using the Docker-Compose instruction file. Learn more about installing Docker-Compose in the Docker documentation.

2. Install and run Email Listener:
1. Open the directory to deploy Email Listener on the server dedicated for the service.

2. Download and unpack the archive that contains the setup files to the directory.

3. Open the / Creatio Email Listener component directory and run the following command:





      ```cli
      docker-compose up -d
      ```





      The command might take up to several minutes to complete.
3. Make sure the logs contain no errors by running the following command: docker logs ListenerAPI.

4. Check whether the deployment is complete by opening the [http://localhost:10000/](http://localhost:10000/) URL, where localhost is the URL of the Email Listener server.


## Set up the Email Listener service in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#title-2111-5 "Direct link to Set up the Email Listener service in Creatio")

1. Make sure the ExchangeListenerService anonymous service is available at **Creatio application address** /0/ServiceModel/ExchangeListenerService.svc (Fig. 2).
Fig. 2 Exchange Listener service response

![Fig. 2 Exchange Listener service response](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/exchange_listener/chapter_exchange_listener_creatio.png)

2. Set the needed system setting values. To do this:
1. Open the System Designer, e. g., by clicking ![btn_system_designer.png](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/exchange_listener/btn_system_designer.png).

2. Click "System settings" in the "System setup" block.

3. Set the values of the following system settings:

      " **ExchangeListenerServiceUri**" (the "ExchangeListenerServiceUri" code). The format of the system setting: **the service address used at installation** /api/listeners.

      " **Creatio exchange events endpoint URL**" (the "BpmonlineExchangeEventsEndpointUrl" code). The format of the system setting value: **the anonymous ExchangeListenerService address** /NewEmail. For example, `https://mycreatio.com/0/ServiceModel/ExchangeListenerService.svc/NewEmail`.

## Email Listener service diagnostics [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#title-2111-6 "Direct link to Email Listener service diagnostics")

The Email Listener service diagnostics page provides tools for troubleshooting the service.

Use the service page:

- to check if the features essential for Exchange Listener are enabled
- to verify the service availability
- to receive subscription information
- to validate the "ExchangeListenerServiceUri" system setting
- to check the health of a mailbox
- to check if the microservice can connect to the Creatio website

You can open the Email Listener service diagnostics page in several ways:

- Use the menu on the Email tab of the communication panel (Fig. 3).
- Use the page of the configured mail services.
- Add the "/0/ClientApp/#/IntegrationDiagnostics/" string to the URL of your Creatio website in the browser address bar and press Enter. For example, `http://mycreatio.com/0/ClientApp/#/IntegrationDiagnostics/ExchangeListener`.

Fig. 3 Open the Email Listener service diagnostics

![Fig. 3 Open the Email Listener service diagnostics](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/exchange_listener/scr_open_diagnostics_page.png)

The diagnostics page contains several readout blocks and diagnostics controls (Fig. 4). By default, most of the readout blocks do not display diagnostics data unless you click **Run diagnostics** in that block.

Fig. 4 Email Listener service diagnostics

![Fig. 4 Email Listener service diagnostics](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/exchange_listener/chapter_exchange_listener_diagnostics_page_full.png)

|     |     |
| --- | --- |
| Feature state | This readout block runs diagnostics automatically on page load.<br>Checks if Email Listener features are enabled in your Creatio application:<br>- ExchangeListenerEnabled<br>- EmailIntegrationV2<br>- SendEmailsV2<br>Learn more about enabling features in the developer documentation: [Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631). |
| Service availability verification | Checks if the Email Listener service is accessible from your Creatio application. |
| Receiving subscription information | Checks the connection to the remote server. |
| Validation of the "ExchangeListenerServiceUri" system setting | Checks if the Exchange Listener service endpoint specified in the "ExchangeListenerServiceUri" system setting is valid. |
| Checking mailbox health | Checks the operation of Microsoft Exchange mailboxes. Select the **Send test email** checkbox to send a test email to the specified address when clicking the **Run diagnostics** link. |

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#see-also "Direct link to See also")

[Add IMAP/SMTP email provider](https://academy.creatio.com/documents?id=1415)

[Set up the Microsoft Exchange and Microsoft 365 services](https://academy.creatio.com/documents?id=1418)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service\#resources "Direct link to Resources")

[Tech Hour - Docker for Creatio](https://www.youtube.com/watch?v=cwTI8pIa_5g&list=PLnolcTT5TeE3v8WGd3VqlZSd2D02GWSGa&index=4)

- [Determine the configuration of the Email Listener service](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#title-2111-7)
  - [Component replica system requirements](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#title-2111-8)
- [Email Listener deployment methods](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#title-2111-1)
  - [Deploy the synchronization service via Kubernetes](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#title-2111-2)
  - [Deploy the synchronization service in Docker](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#title-2111-4)
- [Set up the Email Listener service in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#title-2111-5)
- [Email Listener service diagnostics](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#title-2111-6)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/containerized_components/email_listener_synchronization_service#resources)