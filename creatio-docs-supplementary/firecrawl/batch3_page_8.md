<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/rabbit-mq)** (8.3).

Version: 8.2All Creatio products

On this page

A message broker is a software app that facilitates communication between different software applications or systems. It acts as a central hub, that receives, stores, and forwards messages between various components. This allows for asynchronous communication, where systems can send messages without waiting for immediate responses, making applications more scalable, resilient, and efficient.

Creatio uses its own background task execution subsystem to manage the number of concurrent background tasks. This prevents overutilization of resources like the database server, Redis server, CPU, and RAM on Creatio web nodes, ensuring timely responses to user requests while executing background tasks. Out of the box Creatio uses queue stored in web node RAM.

You can integrate RabbitMQ as a message broker. It helps to **facilitate the Message Bus background task execution subsystem**. The Message Bus system is used to run background parts of business processes (when **Run following elements in the background** or **Run current and the following elements in the background** checkboxes are selected in the Business Process Designer) and can also be used directly through the C# code of the **Script task** element.

Key reasons to integrate RabbitMQ with Creatio:

- **Reliability**. All background tasks will be stored in the RabbitMQ instance, so a reboot or crash of a Creatio instance will not affect the background task queue.



note





Message brokers offer "at least once" delivery, necessitating idempotency in message handlers to prevent duplicate processing. While "at least once delivery" is guaranteed, exactly-once delivery is not. System crashes during long-running processes can lead to data loss or incomplete execution.

- **Scalability**. All web-farm nodes will consume messages from a single queue, allowing workloads to be distributed evenly across multiple application nodes.

- **Load balancing**. It becomes possible to configure some Creatio nodes to consume messages from the message broker without routing HTTP traffic to these nodes, so resource restrictions on these nodes will not affect the user experience in the runtime.


## RabbitMQ connection and operation modes [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#rabbitmq-connection-and-operation-modes "Direct link to RabbitMQ connection and operation modes")

Upon startup, Creatio establishes a connection to the RabbitMQ instance and switches to broker mode, leveraging RabbitMQ for task queuing and processing.

**In-memory mode**. If the initial connection attempt fails or the connection is lost during operation, Creatio transitions to in-memory mode. In this mode, tasks are temporarily stored in memory until the connection to RabbitMQ is restored.

**Task scheduling and processing**. When a new background task is scheduled, Creatio publishes a message to RabbitMQ, containing essential information about the task, including the user context. The message is routed to the `creatio_main` queue, where it is consumed and processed by a Creatio node.

**Log tracking**. Creatio records mode changes in the ServiceBus.log file. To check the current mode of a specific node, access the following URL: `https://creatio-instance/0/ServiceModel/MessageBusManagementService.svc/GetStatistics`.

Fig. 1 RabbitMQ workflow

![Fig. 1 RabbitMQ workflow](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/On-site_deployment/rabbitmq/scr_rabbitmq_workflow.png)

For a deeper understanding of message broker interactions, refer to the [RabbitMQ official documentation](https://www.rabbitmq.com/tutorials/amqp-concepts#amqp-model).

## Set up RabbitMQ integration [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#set-up-rabbitmq-integration "Direct link to Set up RabbitMQ integration")

Before deploying RabbitMQ, ensure that your resources follow the resource allocation recommendations:

- **Shared RabbitMQ instance**. If you are going to use both the Email Listener and Creatio, a single RabbitMQ instance can be shared across both applications.

- **Equal resource allocation**. If you don't use the Email Listener, allocate equal resources to each RabbitMQ node for optimal performance.



| vCPU | RAM | Disk space |
| --- | --- | --- |
| 0.5 | 4 GB | 10 GB |


**Kubernetes resource limits** for RabbitMQ:

- Set absolute memory limit. Configure an absolute memory limit in the RabbitMQ configuration file.
- Allocate sufficient RAM. Ensure the Kubernetes pod's RAM limit is at least twice the configured RabbitMQ memory limit.
- Set recovery time. Set a generous liveness probe timeout (e.g., 5 minutes) to accommodate potential recovery delays, especially for single-virtual-host setups with typical Creatio queues and exchanges.

The **general setup procedure** consists of the following steps:

1. Deploy the RabbitMQ instance.
2. Create a virtual host.
3. Create a new user in RabbitMQ for Creatio integration and grant sufficient permissions to the created user.
4. Update the ConnectionStrings.config file in Creatio.
5. Enable the automatic broker mode in the Web.config file for .NET Framework or in the Terrasoft.WebHost.dll.config file for .NET in the Creatio root directory.

Learn more about the steps performed in RabbitMQ: [RabbitMQ official documentation](https://www.rabbitmq.com/docs/download#installation-guides).

### Setup in RabbitMQ [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#setup-in-rabbitmq "Direct link to Setup in RabbitMQ")

#### Deploy RabbitMQ [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#deploy-rabbitmq "Direct link to Deploy RabbitMQ")

Rabbit MQ offers a variety of **installation options** to cover different needs. Review the available options and select the one that best fits your requirements.

- A **single-node** RabbitMQ setup is the simplest configuration. This setup option offers the advantage of storing background task queues outside of Creatio web nodes. This allows for persistence on disk, ensuring that tasks are not lost even if Creatio restarts.

However, this setup has a significant drawback: a single point of failure. If the RabbitMQ server goes down, your background tasks will be disrupted, and any queued tasks might be lost, depending on the configuration.

Instructions: [RabbitMQ official documentation](https://www.rabbitmq.com/docs/download#installation-guides).

- A **clustered** RabbitMQ deployment is a more robust configuration that involves multiple RabbitMQ nodes working together. This setup option offers high availability, meaning that if one node fails, other nodes can take over its workload. This redundancy significantly reduces the risk of downtime and data loss.

Out of the box, Creatio uses [quorum queues](https://www.rabbitmq.com/docs/quorum-queues#overview), that ensures a highly available solution in a clustered deployment without configuring additional components. You can also disable quorum queue usage if your RabbitMQ instance (for example Amazon MQ) does not support them.

Instructions: [RabbitMQ official documentation](https://www.rabbitmq.com/kubernetes/operator/install-operator).


#### Create a virtual host and a new user [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#create-a-virtual-host-and-a-new-user "Direct link to Create a virtual host and a new user")

If your RabbitMQ is **deployed in Docker**, run the following commands:

```cli
docker exec rabbitmq rabbitmqctl add_vhost creatio
docker exec rabbitmq rabbitmqctl add_user creatio_user changeme
docker exec rabbitmq rabbitmqctl set_permissions -p creatio creatio_user ".*" ".*" ".*
```

If you manage your RabbitMQ via **RabbitMQ Management UI**:

1. **Open** RabbitMQ Management UI in your web browser.

2. **Log in** using your RabbitMQ credentials.

3. **Add a new virtual host**:
1. Go to the **Admin** tab at the top of the page.
2. Click **Add a new virtual host** in the **Virtual Hosts** section.
3. Enter the name of the new virtual host, for example, "creatio."
4. Click **Add virtual host**.
4. **Add a new user**:
1. Scroll down to the **Users** section in the **Admin** tab → click **Add a user**.
2. Enter the username and password.
3. Choose tags for the user, for example, "creatio\_user" for admin privileges.
4. Click **Add user**.
5. **Set permissions for the user**:
1. Click on the newly created user in the list of the **Users** section.
2. Click **Add a permission** under the **Permissions** section.
3. Select the virtual host you created.
4. Set the permissions (`.*` to configure, write, and read).
5. Click **Set permission**.

### Setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#setup-in-creatio "Direct link to Setup in Creatio")

**Update the ConnectionStrings.config file** in the Creatio root directory.

1. **Go to the root directory** of the Creatio application.

2. **Open** the ConnectionStrings.config file.

3. **Specify the connection parameters** for RabbitMQ.





```xml
<add name="messageBroker" connectionString="amqp://creatio_user:changeme@localhost:5672/creatio" />
```

4. **Save the changes**.


**Enable the automatic broker mode** in the the Web.config file for .NET Framework or in the Terrasoft.WebHost.dll.config for .NET.

1. **Go to the root directory** of the Creatio application.

2. **Open** the Web.config file for .NET Framework or the Terrasoft.WebHost.dll.config for .NET.

3. **Go to ~/configuration/serviceBus** and set `operatingMode="Auto"`.





```xml
<!-- OperatingMode determines a message bus operating mode. Possible values are: InMemory and Auto. -->
<serviceBus incomingQueueName="creatio_main" defaultSendAddress="exchange:creatio_exchange" operatingMode="Auto" messageProcessingThreadsCount="10" />
```

4. **Save the changes**.


## Monitor RabbitMQ [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#monitor-rabbitmq "Direct link to Monitor RabbitMQ")

A robust logging strategy is crucial for effective monitoring, troubleshooting, and security in a RabbitMQ environment. By carefully configuring and collecting logs, you can gain valuable insights into the health and performance of your message broker. This step is optional but recommended. Instructions: [RabbitMQ official documentation](https://www.rabbitmq.com/docs/logging).

Include RabbitMQ server in your monitoring system. This also will be useful to analyze amount of background tasks Creatio is executing and current queue size. Consider monitoring:

- consumers count (must be 1 per Creatio node)
- `creatio_main` queue size
- `creatio_main_error` queue size (must be zero)
- publish/consumption rate
- available memory
- free disk space

Instructions: [RabbitMQ official documentation](https://www.rabbitmq.com/docs/prometheus).

## Update RabbitMQ [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#update-rabbitmq "Direct link to Update RabbitMQ")

You can update your RabbitMQ instance in multiple ways:

- Deploy a new version alongside the existing version
- Upgrade the existing instance/cluster

### Deploy a new version alongside the existing version [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#deploy-a-new-version-alongside-the-existing-version "Direct link to Deploy a new version alongside the existing version")

You can use this way if RabbitMQ is exclusively used by Creatio and you have scheduled maintenance windows.

1. Deploy the newer version of RabbitMQ.
2. Set up virtual host and user for Creatio.
3. Switch to the new instance.
4. If the old RabbitMQ instance contains messages that need to be preserved, [utilize the Shovel Plugin](https://www.rabbitmq.com/docs/shovel)`rabbitmq_shovel` to transfer these messages to the new instance. This ensures a seamless transition and avoids data loss.

Alternatively, consider a more complex approach outlined in the RabbitMQ documentation: [Upgrading RabbitMQ Using Blue-Green Deployment Strategy](https://www.rabbitmq.com/docs/blue-green-upgrade). This strategy involves deploying a new RabbitMQ instance alongside the existing instance, gradually migrating traffic to the new instance, and then decommissioning the old instance.

### Upgrade the existing instance of RabbitMQ [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#upgrade-the-existing-instance-of-rabbitmq "Direct link to Upgrade the existing instance of RabbitMQ")

Certain Creatio queues are replicated across multiple RabbitMQ nodes. When updating a RabbitMQ cluster that gas quorum queues, it is essential to upgrade one node at a time to avoid potential inconsistencies and data loss. Learn more: [RabbitMQ official documentation](https://www.rabbitmq.com/docs/upgrade#quorum-queues).

If you use the RabbitMQ Kubernetes Operator, upgrading to a newer version typically involves updating the operator manifest. Learn more: [RabbitMQ official documentation](https://www.rabbitmq.com/kubernetes/operator/upgrade-operator#overview).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq\#see-also "Direct link to See also")

[Modify ConnectionStrings.config for MS SQL Server](https://academy.creatio.com/documents?id=2138)

[Modify ConnectionStrings.config for Oracle Database](https://academy.creatio.com/documents?id=2139)

[Modify ConnectionStrings.config for PostgreSQL](https://academy.creatio.com/documents?id=2140)

[RabbitMQ official documentation](https://www.rabbitmq.com/docs)

- [RabbitMQ connection and operation modes](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#rabbitmq-connection-and-operation-modes)
- [Set up RabbitMQ integration](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#set-up-rabbitmq-integration)
  - [Setup in RabbitMQ](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#setup-in-rabbitmq)
  - [Setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#setup-in-creatio)
- [Monitor RabbitMQ](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#monitor-rabbitmq)
- [Update RabbitMQ](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#update-rabbitmq)
  - [Deploy a new version alongside the existing version](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#deploy-a-new-version-alongside-the-existing-version)
  - [Upgrade the existing instance of RabbitMQ](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#upgrade-the-existing-instance-of-rabbitmq)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/rabbit-mq#see-also)