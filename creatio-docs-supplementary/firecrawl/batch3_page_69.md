<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux)** (8.3).

Version: 8.2All Creatio products

On this page

Important

Since Microsoft ended official support for .NET 6 in November 2024, starting from version 8.2.1 Creatio no longer supports .NET 6 and switches to .NET 8.

Before you deploy the server, take the following steps:

- Prepare the Creatio setup files. [Read more >>>](https://academy.creatio.com/documents?id=2120)
- Deploy the database server. [Read more >>>](https://academy.creatio.com/documents?id=2121)
- Deploy the Creatio caching server (Redis). [Read more >>>](https://academy.creatio.com/documents?id=2108)
- Modify the ConnectionStrings.config file. [Read more >>>](https://academy.creatio.com/documents?id=2122)

note

Learn more about running a PostgreSQL server in Docker in the [Docker documentation](https://hub.docker.com/r/library/postgres/).

## Method 1. Deploy Creatio .NET on Linux directly [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2649-1 "Direct link to Method 1. Deploy Creatio .NET on Linux directly")

To deploy the Creatio application server:

- Install .NET, a GDI+ compatible API for UNIX-like operating systems, and development libraries and header files for GNU C. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2649-2)
- Run the Creatio application server. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2649-3)

### Install .NET and other Creatio dependencies [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2649-2 "Direct link to Install .NET and other Creatio dependencies")

01. Download the packages-microsoft-prod package:





    ```cli
    wget -q https://packages.microsoft.com/config/ubuntu/[latests LTS version]/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
    ```

02. Log in as root:





    ```cli
    sudo su
    ```

03. Install the downloaded package:





    ```cli
    dpkg -i packages-microsoft-prod.deb
    ```

04. Update the package lists:





    ```cli
    apt-get update
    ```

05. Install the APT transport for downloading via the HTTP Secure protocol:





    ```cli
    apt-get install apt-transport-https
    ```

06. Update the package lists:





    ```cli
    apt-get update
    ```

07. Install .NET:





    ```cli
    apt-get install dotnet-sdk-[version]
    ```





    where `sdk-[version]` is the latest package version. For example, `apt-get install dotnet-sdk-8.0`.

08. Install a GDI+ compatible API for non-Windows operating systems:





    ```cli
    apt-get install -y libgdiplus
    ```

09. Install development libraries and header files for GNU C:





    ```cli
    apt-get install -y libc6-dev
    ```

10. Log out from your root session:


```cli
exit
```

### Run the Creatio application server [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2649-3 "Direct link to Run the Creatio application server")

note

If you are deploying the .NET development environment that has access via HTTP, modify the Terrasoft.WebHost.dll.config file in the Creatio root directory before you run Creatio. Set the "add key" parameter to the following: `<add key="CookiesSameSiteMode" value="Lax" />`

This ensures correct operation both via HTTP and HTTPS. However, the mobile app will not be operational if you use this setting.

To run Creatio:

1. Open the directory that contains Creatio setup files:





```cli
cd /path/to/application/directory/
```

2. Run the .NET server:





```cli
COMPlus_ThreadPool_ForceMinWorkerThreads=100 dotnet Terrasoft.WebHost.dll
```


Creatio HTTP version will be available on port 5000.

Creatio HTTPS version will be available on port 5002.

note

To log in to newly deployed Creatio, use the default Supervisor user account. It is highly recommended to change the Supervisor password immediately. Login: Supervisor; password: Supervisor.

## Method 2. Deploy Creatio .NET on Linux using Docker [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2649-4 "Direct link to Method 2. Deploy Creatio .NET on Linux using Docker")

Use this deployment method to run a compartmentalized Creatio application. We assume that you have installed the Redis sever, deployed the Creatio database, and set up the ConnectionStrings.config file using the instructions in the previous steps.

To deploy Creatio application server using Docker:

- Make Redis accessible from the Docker container. [Read more >>>](https://academy.creatio.com/documents?id=2126)
- Install Docker. [Read more >>>](https://academy.creatio.com/documents?id=2127)
- Create a Dockerfile. [Read more >>>](https://academy.creatio.com/documents?id=2128)
- Build and run a Docker image. [Read more >>>](https://academy.creatio.com/documents?id=2129)

Important

We recommend deploying Creatio using Docker for development and testing environments only. Avoid using Docker for the production environment.

### Configure the Creatio caching server (Redis) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2649-5 "Direct link to Configure the Creatio caching server (Redis)")

1. Open **redis.conf** in a text editor as root. For example, use the Nano text editor:





```cli
sudo nano /etc/redis/redis.conf
```

2. Locate the " **bind 127.0.0.1 ::1**" entry. Replace the entry with " **bind 0.0.0.0**" to listen to all available IPV4 interfaces.

3. Save changes and exit the editor.

4. Restart the Redis server:





```cli
sudo systemctl restart redis-server
```


### Install Docker [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2649-6 "Direct link to Install Docker")

To install Docker, run:

```cli
sudo apt-get install docker
```

#### Create a Dockerfile [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2649-7 "Direct link to Create a Dockerfile")

1. Open the Creatio directory:





```cli
cd /path/to/application/directory/
```





**/path/to/application/directory/** is the directory that contains unpacked Creatio installation files.

2. Create a Dockerfile using a text editor. For example, use the Nano text editor:





```cli
nano Dockerfile
```

3. Insert the following code:





```cli
FROM mcr.microsoft.com/dotnet/sdk:[version] AS base
EXPOSE 5000 5002
RUN apt-get update && \
apt-get -y --no-install-recommends install \
libgdiplus \
libc6-dev && \
apt-get clean all && \
rm -rf /var/lib/apt/lists/* /var/cache/apt/*
WORKDIR /app
COPY . ./
FROM base AS final
WORKDIR /app
ENV ASPNETCORE_ENVIRONMENT Development
ENV TZ US/Eastern
ENV COMPlus_ThreadPool_ForceMinWorkerThreads 100
ENTRYPOINT ["dotnet", "Terrasoft.WebHost.dll"]
```





where `sdk:[version]` is the latest package version. For example, `mcr.microsoft.com/dotnet/sdk:8.0`.

4. Press Ctrl+O to save the changes.

5. Press Ctrl+X to exit the editor.


#### Build and run a Docker image [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2649-8 "Direct link to Build and run a Docker image")

note

If you are deploying the .NET evelopment environment witthat has access via HTTP, modify the Terrasoft.WebHost.dll.config file in the Creatio root directory before you run the Docker image. Set the "add key" parameter to the following: `<add key="CookiesSameSiteMode" value="Lax" />`.

This ensures correct operation both via HTTP and HTTPS. However, the mobile app will not be operational if you use this setting.

Build a Docker image:

```cli
docker build -f Dockerfile -t creatioimg .
```

Run the docker image:

```cli
docker run -p http_port_number:5000 -p https_port_number:5002 -d --dns=DNS_server_ip --dns-search=DNS_address_suffix -v /logspath/mycreatio:/app/Logs --name Creatio creatioimg
```

**http\_port\_number** is a port number. Docker will serve the HTTP version on this port

**https\_port\_number** is a port number. Docker will serve the HTTPS version on this port

**DNS\_server\_ip** is the IP address of a DNS server that enables the container to resolve Internet domains. You can use multiple **--dns** flags for multiple DNS servers.

**DNS\_address\_suffix** is a DNS search domain that enables the container to search for non-fully-qualified hostnames. You can use multiple **--dns-search** flags for multiple DNS search domains.

note

Add the --restart=always flag to the command make a persistent Docker container.

Creatio HTTP version will be available on port **http\_port\_number**.

Creatio HTTPS version will be available on port **https\_port\_number**.

note

To log in to a newly deployed application, use the default Supervisor user account. It is highly recommended to change the Supervisor password immediately. Login: Supervisor; password: Supervisor.

## Configure Creatio .NET for HTTPS [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#title-2497-17 "Direct link to Configure Creatio .NET for HTTPS")

Before you start working in Creatio via HTTPS, take the following steps:

1. Obtain a \*.pfx digital certificate from the certification center.



note





If you use a self-signed certificate, Creatio mobile application cannot connect to the Creatio website due to security policies of mobile applications.

2. Go to Creatio root directory and open appsettings.json.

3. Specify your website address, path to the certificate, and certificate password in the "Https" block.


Example of the Https block in appsettings.json

```json
"Https": {
    "Url": "https://::5002",
    "Certificate": {
        "Path": "C:\Projects\site\20210215_103239\localhost.pfx",
        "Password": "Password"
    }
}
```

note

You can specify both relative and absolute path to the certificate. The absolute path must be JSON compatible.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux\#see-also "Direct link to See also")

[Enable required Windows components](https://academy.creatio.com/documents?id=2081)

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [Method 1. Deploy Creatio .NET on Linux directly](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2649-1)
  - [Install .NET and other Creatio dependencies](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2649-2)
  - [Run the Creatio application server](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2649-3)
- [Method 2. Deploy Creatio .NET on Linux using Docker](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2649-4)
  - [Configure the Creatio caching server (Redis)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2649-5)
  - [Install Docker](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2649-6)
- [Configure Creatio .NET for HTTPS](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#title-2497-17)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux#see-also)