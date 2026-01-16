<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/general-setup-procedure-for-data-caching-server-redis#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/caching-server/general-setup-procedure-for-data-caching-server-redis)** (8.3).

Version: 8.2All Creatio products

On this page

Use Redis caching server to optimize execution of heavy database queries. Caching improves Creatio performance and reduces the resource usage.

note

Creatio lets you use Amazon ElastiCache for Redis. If you want to use Amazon ElastiCache, follow the general Redis setup procedure in Creatio. Learn more about setting up Amazon ElastiCache in AWS in the official AWS documentation: [Getting started with Amazon ElastiCache for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/GettingStarted.html).

The Redis server package is available in the standard Debian repositories. This article covers installing Redis on Debian and Debian derivatives (such as Ubuntu and Linux Mint). To install Redis:

1. Log in as root:





```cli
sudo su
```

2. Update the package lists:





```cli
apt-get update
```

3. Install Redis:





```cli
apt-get install redis-server
```

4. Enable Redis to run as a **systemd** service. To do this:
1. Open **redis.conf** in a text editor as root. For example, use the Nano text editor:





      ```cli
      nano /etc/redis/redis.conf
      ```

2. Locate the " **supervised no**" entry. Replace the entry with " **supervised systemd**."

3. Save changes and exit the editor.

4. Restart the Redis server.





      ```cli
      systemctl restart redis-server
      ```

5. Log out from your root session:





      ```cli
      exit
      ```

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/general-setup-procedure-for-data-caching-server-redis\#see-also "Direct link to See also")

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?id=2136)

[Deploy the Creatio .NET Core application server on Linux](https://academy.creatio.com/documents?product=administration&ver=7&id=2148)

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/caching-server/general-setup-procedure-for-data-caching-server-redis#see-also)