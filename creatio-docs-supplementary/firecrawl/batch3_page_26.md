<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/application-server-web-farm)** (8.3).

Version: 8.2All Creatio products

On this page

You can enhance the performance of large-scale Creatio projects (up to several thousand users) through horizontal scaling, i. e., by increasing the number of servers with deployed Creatio applications and setting up workload distribution between them.

The load balancer may be either hardware or software. To work in fault-tolerant mode, use an HTTP/HTTPS traffic balancer that supports the WebSocket protocol. Creatio has been tested on the HAProxy software load balancer. There are cases of successful implementation of other balancers, e. g., Citrix, Cisco, NginX, FortiGate, Microsoft ARR.

note

The installation procedure of Marketplace add-ons and custom improvements for an environment that uses a balancer differs from the standard deployment process. Learn more in a separate article: [Install applications from the Marketplace](https://academy.creatio.com/documents?id=1835).

This guide covers horizontal scaling of Creatio using a free open-source load balancer (HAProxy), designed for distributing the load between several application servers.

note

Synchronize the server time of the nodes (servers and computers) that run deployed application instances to ensure smooth operation of Creatio.

## General deployment procedure [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-1 "Direct link to General deployment procedure")

### Creatio .NET Framework [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-10 "Direct link to Creatio .NET Framework")

To deploy Creatio using the horizontal scaling of **.NET Framework** application servers:

01. Deploy the required number of Creatio application instances in a web farm.



    note





    We recommend specifying identical names in IIS and the Application pool setting for all Creatio instances.

02. Specify identical SQL and Redis databases in the ConnectionStrings.config file for all instances.





    ```xml
    <add name="redis" connectionString="host=DOMAIN.COM;db=0;port=6379;maxReadPoolSize=10;maxWritePoolSize=500"/>
    <add name="db" connectionString="Data Source=DOMAIN.COM;Initial Catalog=DatabaseName;Integrated Security=SSPI; MultipleActiveResultSets=True;Pooling-true;Max Pool Size=100"/>
    ```

03. Add the following key in the `<appSettings>` block of the application’s Web.config file:





    ```xml
    <add key="TenantId" value="1" />
    ```









    The “value” number must be identical for all Creatio instances of the web farm.



    Important





    Starting with Creatio version 7.14.1, the `<add key="TenantId" value="..."/>` key can only be added to the internal Web.config file (Terrasoft.WebApp\\Web.config). Adding the key to an external Web.config file may lead to application failures.

04. Generate a unique machineKey value for one of Creatio instances. Learn more in a separate article: [Modify Web.config](https://academy.creatio.com/documents?id=2141). Copy the resulting value and specify it in the Web.config files of each Creatio instance. You can locate the files in the root Creatio folder and the Terrasoft.WebApp folder.

05. Turn on clustering for all schedulers in the `<quartzConfig>` block of every node's external configuration file (Web.config):





    ```xml
    <add key="quartz.jobStore.clustered" value="true" />
    <add key="quartz.jobStore.acquireTriggersWithinLock" value="true" />
    ```

06. If the instanceId settings collide, specify unique values for each scheduler node.

    The **ways to specify** unique instanceId values are as follows:
    - Add the following string to all schedulers in the `<quartzConfig>` block of every node’s external configuration file (Web.config):





      ```xml
      <add key="quartz.scheduler.instanceId" value="AUTO" />
      ```











      Important





      The “AUTO” value of the “value” attribute must be uppercase. Otherwise, Creatio will treat the value as the node name, which may lead to errors in the scheduler’s operation.





      As a result, the scheduler will generate the unique node name based on the `<node name>+timestamp` template.

    - Add unique quartz.scheduler.instanceId values manually.
07. Set the “value” attribute of the quartz.jobStore.clustered setting to “true.”





    ```xml
    <add key="quartz.jobStore.clustered" value="true" />
    ```

08. Grant access permissions to created application directories for the IUSR user and the user who launches the Application pool in IIS.

09. Set up a load balancer (e. g., HAProxy) to distribute the workload between the deployed application servers.

10. If necessary, set up load balancing for database and session servers.



    note





    Learn more about setting up clustering in the [Microsoft SQL](https://docs.microsoft.com/en-us/sql/sql-server/failover-clusters/install/create-a-new-sql-server-failover-cluster-setup?view=sql-server-2017) and [Oracle](https://docs.oracle.com/cd/B28359_01/rac.111/b28254/admcon.htm#i1058057) documentation. Learn more about setting up fault tolerance using Redis Cluster in a separate article: [Redis Cluster](https://academy.creatio.com/documents?id=2349).


### Creatio .NET Core [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-11 "Direct link to Creatio .NET Core")

To deploy Creatio using the horizontal scaling of **.NET Core** application servers:

01. Deploy the required number of [Creatio application instances](https://academy.creatio.com/documents?id=2124).

02. Specify identical SQL and Redis databases in the [ConnectionStrings.config file](https://academy.creatio.com/documents?id=2120) for all instances.

03. Go to the root directory of any Creatio instance and locate the Terrasoft.WebHost.dll file.

04. Run the following command:





    ```cs
    dotnet Terrasoft.WebHost.dll configureWebFarmMode
    ```









    As a result, configuration files of the current application instance will be updated.

05. Enable clustering for all schedulers in the `<quartzConfig>` block of every node's external configuration file (Terrasoft.WebHost.dll):





    ```xml
    <add key="quartz.jobStore.clustered" value="true" />
    <add key="quartz.jobStore.acquireTriggersWithinLock" value="true" />
    ```

06. If the instanceId settings collide, specify unique values for each scheduler node.

    The **ways to specify** unique instanceId values are as follows:
    - Add the following string to all schedulers in the `<quartzConfig>` block of every node’s external configuration file (Terrasoft.WebHost.dll):





      ```xml
      <add key="quartz.scheduler.instanceId" value="AUTO" />
      ```











      Important





      The “AUTO” value of the “value” attribute must be uppercase. Otherwise, Creatio will treat the value as the node name, which may lead to errors in the scheduler’s operation.





      As a result, the scheduler will generate the unique node name based on the `<node name>+timestamp` template.

    - Add unique quartz.scheduler.instanceId values manually.
07. Set the “value” attribute of the quartz.jobStore.clustered setting to “true.”





    ```xml
    <add key="quartz.jobStore.clustered" value="true" />
    ```

08. If necessary, set up load balancing for the database and session servers.

09. Copy all configuration files of the current application instance to the root folders of other application instances.

10. Set up a load balancer (e. g., HAProxy) to distribute the workload between the deployed application servers.


note

Learn more about setting up clustering in the DBMS vendor documentation. Learn more about setting up fault tolerance using Redis Cluster in a separate article: [Redis Cluster](https://academy.creatio.com/documents?id=2349).

## Install the HAProxy balancer [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-2 "Direct link to Install the HAProxy balancer")

The HAProxy load balancer supports a range of free open-source OS. This guide covers one of the simpler methods of deploying HAProxy on the Debian OS via the haproxy.debian.net service.

1. Open the installation service page by clicking [https://haproxy.debian.net/](https://haproxy.debian.net/).

2. Select the OS and its version, as well as the HAProxy version.



note





Use the cat /etc/issue command to check the currently installed Debian version.





As a result, the service will generate a set of HAProxy installation commands to run in the Debian OS.
Fig. 1 HAProxy installation commands generated by the haproxy.debian.net service

![Fig. 1 HAProxy installation commands generated by the haproxy.debian.net service](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/app_server_webfarm/haproxy_settings_commands.png)

3. Run the generated commands one after another.


## Set up the HAProxy balancer [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-3 "Direct link to Set up the HAProxy balancer")

To set up HAProxy, modify the haproxy.cfg file. Follow this path to locate the file:

```cli
.../etc/haproxy/haproxy.cfg
```

### Primary setup (required) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-4 "Direct link to Primary setup (required)")

Add the sections required for HAProxy operation: **frontend** and **backend**.

#### The frontend section [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-5 "Direct link to The frontend section")

Add the following settings to the frontend section: **bind** and **default\_backend**.

- Specify the address and the port that will receive requests distributed by HAProxy in the **bind** setting.
- Specify the name that will match the name of the backend section in the **default\_backend** option.

As a result, the setting will look as follows:

```cli
frontend front
maxconn 10000
#Using these ports for binding
bind *:80
bind *:443
#Convert cookies to be secure
rspirep ^(set-cookie:.*)  \1;\ Secure
default_backend creatio
```

#### The backend section [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-6 "Direct link to The backend section")

Add the following required settings to the backend section:

- Specify the type of balancing, e. g., **roundrobin**, in the **balance** parameter. Learn more about the different types of balancing in the [HAProxy documentation](https://cbonte.github.io/haproxy-dconv/configuration-1.5.html#4.2-balance).
- Use the **server** parameter to specify all servers (or nodes) that distribute the load.

Add a unique “server” parameter that contains the server address, port address, and weight for each server (i. e. the deployed Creatio instance). The server weight enables the balancer to distribute the load based on the physical capabilities of the servers. The higher weight you specify for the server, the more requests it will receive. For example, if you need to distribute the load between 2 Creatio application servers, add 2 “server” parameters to backend:

```cs
server node_1 [server address]:[port] weight
server node_2 [server address]:[port] weight
```

As a result, the setting will look as follows:

```cli
backend creatio
#set balance type
balance roundrobin

server node_1 nodeserver1:80 check inter 10000 weight 2
server node_2 nodeserver2:80/sitename check inter 10000 weight 1
```

The new settings will be applied as soon as you restart HAProxy. Use the following command to restart HAProxy:

```js
service haproxy restart
```

### Check the server status [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-7 "Direct link to Check the server status")

The HAProxy balancer works with the following server statuses:

| Status | Description |
| --- | --- |
| UP | The server is operational. |
| UP - transitionally DOWN | The server is considered operational at the moment, but the last health check has failed. As a result, the server is currently switching to the DOWN status. |
| DOWN - transitionally UP | The server is not considered operational at the moment, but the last health check has succeeded. As a result, the server is currently switching to the UP status. |
| DOWN | The server is not operational. |

Health checks initiate changes in a server’s operational status. The simplest health check requires adding the “check” keyword to the server setup string. Running the health check requires the server’s IP and TCP port. Health check example:

```cli
server node1 ... check
option httpchk GET /Login/NuiLogin.aspx
option httpchk GET /0/ping
```

### Set up web stats (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-8 "Direct link to Set up web stats (optional)")

To turn on web stats, add a new listen section that contains the following parameters: **bind**, **mode http**, **stats enable**, **stats uri**. The section will look as follows:

```cli
listen stats # Define a listen section called "stats"
    bind :9000 # Listen on localhost:9000
    mode http
    stats enable # Enable stats page
    stats uri /haproxy_stats # Stats URI
```

As a result, you will be able to view the web stats of Creatio load balancing in the browser.

Fig. 2 The web stats of the load balancer

![Fig. 2 The web stats of the load balancer](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/app_server_webfarm/load_balancer_stats.png)

To view the stats, follow the path: **balancer address**:9000/haproxy\_stats.

### Set up the IP addresses in the audit log for .NET Core (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-19 "Direct link to Set up the IP addresses in the audit log for .NET Core (optional)")

With a web farm, user requests reach the servers through a load balancer and/or a proxy server. As such, by default, the [audit log](https://academy.creatio.com/documents?id=2320) displays the IP address of the proxy that forwarded the request last, not the actual IP address of the user.

You can configure the audit log so that it displays the actual IP address of the user. To do this:

1. Configure the balancer so that each request it forwards to one of the Creatio application instances has a header with “ForwardedForHeaderName” name and the user’s IP address value.

2. Modify the configuration files of Creatio application instances accordingly.
1. Go to Creatio root directory and open appsettings.json.

2. Edit the “ForwardedHeaders” section so that it reads:





      ```js
      {
          ...
          "ForwardedHeaders": {
              "Enable": true,
              "ForwardedForHeaderName": "X-Forwarded-For",
              "KnownProxiesIP": [trusted IP addresses],
              "ForwardLimit": 3
          }
          ...
      }
      ```









      Where:

      “ **Enable**” turns on the Forwarded headers processing function in the web application.

      “ **ForwardedForHeaderName**” is the name of the header that contains the IP address.

      “ **KnownProxiesIP**” is the trusted IP address list. Creatio processes the “ **ForwardedHeader**” value only if it receives a request from these IP addresses. They can belong to the load balancer, reverse proxy, etc. If you leave this value empty, Creatio processes the “ForwardedHeader” value received from any IP address.



      Example





      ```xml
      "KnownProxiesIP": ["127.0.0.1", "12.34.56.78", "2001:0db8:85a3:0000:0000:8a2e:0370:7334"]
      ```









      “ **ForwardLimit**” is the limit of IP addresses in the “X-Forwarded-For” processed header. The parameter adds more protection from incorrectly setup proxy servers and malicious requests received from third-party network channels. Proxy servers write their IP addresses to the end of the “X-Forwarded-For” header when forwarding requests. For example, the “X-Forwarded-For” header can have the following IP address chain: ip1, ip2, ip3, ip4. In this case:


      - ip1 is the client (browser) address.
      - ip2 and ip3 are proxy server addresses.
      - ip4 is the balancer address.

If you set “ForwardLimit” to 4, the web server receives all 4 addresses. If you set it to 3, the web server receives only the last 3 IP addresses, i. e., ip2, ip3, and ip4.

The default value is 3. If you have the “ **KnownProxiesIP**” parameter set up, you can set the “ **ForwardLimit**” parameter to null.

3. Repeat steps a-b for all Creatio application instances in your web farm.

## Host static content separately [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#title-241-20 "Direct link to Host static content separately")

You can host static content of the application on a separate server. While this is usually unnecessary, it can be beneficial in certain scenarios to reduce the loading time of static content. To do this, use NginX as a reverse proxy. All requests for static content are redirected to NginX, which then serves the files from the application directory. From the client perspective, static content is delivered from a separate server located in a more optimal geographic location.

To install NginX, deploy it in Kubernetes. We recommend using the Helm chart from Bitnami [charts/bitnami/nginx at main · bitnami/charts](https://github.com/bitnami/charts/tree/main/bitnami/nginx) with two replicas. Each replica utilizes 100 Mb of CPU and 128 Mb of memory.

Configure the load balancer using the rules below. Redirect requests for static content to the NginX server(s).

- application.creatio.com/\*/terrasoft.axd\* → IIS, Creatio nodes
- application.creatio.com/0/conf/content/\* → NginX server(s)
- application.creatio.com/0/Shell/\* → NginX server(s)
- application.creatio.com/0/core/\* → NginX server(s)
- application.creatio.com/\* → IIS, Creatio nodes

Fig. 3 NginX configuration

![Fig. 3 NginX configuration](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/On-site_deployment/application_server_web_farm/scr_load_balancer.png)

View an example configuration file (nginx.conf) for the NginX server below.

```cli
worker_processes auto;
events {
    worker_connections 10000;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml application/javascript application/json;
    gzip_disable "MSIE [1-6]\.";
    server_tokens off;
    server {
        listen 0.0.0.0:8080;
        location /0/conf/content/ {
            alias /var/www/creatio/content/; # LOCAL PATH TO STATIC CONTANT
            try_files $uri $uri/ =404;
        }
        location /0/Shell/ {
            alias /var/www/creatio/Shell/; # LOCAL PATH TO Shell content
            try_files $uri $uri/ =404;
        }
        location /0/ClientApp/ {
            alias /var/www/creatio/ClientApp/; # LOCAL PATH TO ClientApp content
            try_files $uri $uri/ =404;
        }
    }
}
```

note

System design modifications affect static content. As such, clear the NginX cache after making changes to the application design.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm\#see-also "Direct link to See also")

[Server-side system requirements](https://academy.creatio.com/documents?id=1456)

[Secure access to the portal](https://academy.creatio.com/documents?id=2033)

[Quartz task scheduler](https://academy.creatio.com/documents?id=15801)

[Redis Cluster](https://academy.creatio.com/documents?id=2349)

- [General deployment procedure](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-1)
  - [Creatio .NET Framework](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-10)
  - [Creatio .NET Core](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-11)
- [Install the HAProxy balancer](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-2)
- [Set up the HAProxy balancer](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-3)
  - [Primary setup (required)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-4)
  - [Check the server status](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-7)
  - [Set up web stats (optional)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-8)
  - [Set up the IP addresses in the audit log for .NET Core (optional)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-19)
- [Host static content separately](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#title-241-20)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/application-server-web-farm#see-also)