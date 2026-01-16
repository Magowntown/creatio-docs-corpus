<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/caching-server/set-up-secure-connection-to-redis)** (8.3).

Version: 8.2All Creatio products

On this page

**TLS** (transport layer security) is a cryptographic protocol that facilitates secure data transfer between Internet network nodes. Learn more in [Wikipedia](https://en.wikipedia.org/w/index.php?title=Transport_Layer_Security&oldid=1099038506). Data transfer is open and insecure otherwise.

## Set up the connection via the TLS 1.2 protocol [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis\#title-2389-4 "Direct link to Set up the connection via the TLS 1.2 protocol")

Creatio lets you set up the connection to the following **Redis configurations**:

- standalone (non-clustered)
- Redis Cluster

The general steps to set up the connection to a Redis server via the TLS 1.2 protocol are as follows:

1. Perform the setup in Redis. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis#title-2389-1)
2. Perform the setup in Creatio. [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis#title-2389-2)

### Setup in Redis [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis\#title-2389-1 "Direct link to Setup in Redis")

Redis version 6.0 and later support the TLS protocol. Make sure that your Redis version supports the TLS protocol. To enable the TLS protocol functionality, activate it when you install Redis. To do this, follow the instructions in the [official vendor documentation](https://redis.io/docs/manual/security/encryption/).

### Setup in Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis\#title-2389-2 "Direct link to Setup in Creatio")

1. Set up the connection to Redis via the TLS 1.2 protocol in Creatio. To do this, add the `useTls=true` parameter to the `connectionString` parameter of the ConnectionStrings.config configuration file.

2. Set up the authentication option on the Redis server.

Depending on the settings in Redis, the following **authentication options** are available:
   - Redis server certificate. Enabled by default when you set up the TLS protocol in Redis.
   - Redis server password.
   - Redis server certificate and password

```xml
<connectionStrings>
    ...
    <add name="redis" connectionString="clusterHosts=[SOME_NODE_1_IP:SOME_NODE_1_PORT],...,[SOME_NODE_N_IP:SOME_NODE_N_PORT]; useTls=true; password=SOME_PASSWORD; certificatePath=SOME_CERTIFICATE_PATH; certificatePassword=SOME_CERTIFICATE_PASSWORD" />
</connectionStrings>
```

where

- `clusterHosts` are the IP addresses of Redis server nodes.
- `useTls` controls the use of the TLS 1.2 protocol for the Creatio connection to the Redis server.
- `password` is the password required to authenticate on the Redis server. Set the parameter if you use a password or certificate and password to authenticate on the Redis server. Do not add the parameter otherwise.
- `certificatePath` is the path to the certificate required to authenticate on the Redis server. Set the parameter if you use a certificate or certificate and password to authenticate on the Redis server. Do not add the parameter otherwise.
- `certificatePassword` is the password to the certificate required to authenticate on the Redis server. Required if the Redis server certificate has a password set. Set the parameter if you use a certificate or certificate and password to authenticate on the Redis server. Do not add the parameter otherwise.

note

If the ConnectionStrings.config file has no `useTls` parameter or you set it to `false`, Creatio ignores the `password`, `certificatePath`, `certificatePassword` parameters.

As a result, Creatio will use the TLS 1.2 protocol to connect to the Redis server.

## Disable the validation of the Redis server certificate [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis\#title-2389-3 "Direct link to Disable the validation of the Redis server certificate")

When you use the TLS 1.2 protocol to connect to a Redis server in a development environment, you can disable the certificate validation. This decreases the time to set up the certificate validation. To do this, set the `disableTlsCertificateValidation` parameter in the ConnectionStrings.config configuration file to `true`.

```xml
<connectionStrings>
    ...
    <add name="redis" connectionString="disableTlsCertificateValidation=true, ..." />
</connectionStrings>
```

As a result, Creatio will use the TLS 1.2 protocol to connect to the Redis server without validating the certificate.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis\#see-also "Direct link to See also")

[The concept of TLS protocol](https://en.wikipedia.org/w/index.php?title=Transport_Layer_Security&oldid=1099038506)

[Redis Cluster](https://academy.creatio.com/documents?id=2349)

[Official Redis documentation](https://redis.io/docs/manual/security/encryption/)

- [Set up the connection via the TLS 1.2 protocol](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis#title-2389-4)
  - [Setup in Redis](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis#title-2389-1)
  - [Setup in Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis#title-2389-2)
- [Disable the validation of the Redis server certificate](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis#title-2389-3)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/set-up-secure-connection-to-redis#see-also)