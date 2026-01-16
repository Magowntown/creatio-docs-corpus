<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/database-server/deploy-postgresql-database-linux)** (8.3).

Version: 8.2All Creatio products

On this page

Use one of two database configurations to deploy Creatio:

- Use a remote DBMS (recommended)
- Use a local PostgreSQL server.

If you already have a PostgreSQL server running on the intended machine, skip to step II.

If you have set up sysadmin (with privileges to log in, create and modify databases) and public (unprivileged) user roles, skip to step III.

## I. Install PostgreSQL [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux\#title-250-1 "Direct link to I. Install PostgreSQL")

PostgreSQL is unavailable in most standard repositories. To install PostgreSQL on Linux:

1. Log in as root:





```cli
sudo su
```

2. Add the PostgreSQL repository:





```cli
echo -e "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
```

3. Import the signing key of the PostgreSQL repository:





```cli
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
```

4. Update the package lists:





```cli
apt-get update
```

5. Install PostgreSQL:





```cli
apt-get install -y postgresql-16
```

6. Log out from your root session:





```cli
exit
```


note

Please refer to the [PostgreSQL documenation](https://www.postgresql.org/docs/9.5/high-availability.html) for details on PostgreSQL clustering.

## II. Create PostgreSQL user [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux\#title-250-2 "Direct link to II. Create PostgreSQL user")

A fresh installation of PostgreSQL is not ready for deploying Creatio immediately. If you plan to use a fresh installation of PostgreSQL, you need to create a user that can log in to the database using a password and has sufficient privileges to create and update a database. By default, no such user will be available.

We recommend to create two database users in PostgreSQL:

- A user with the " **sysadmin**" role, who has maximum access privileges on the database server level. This user will restore the Creatio database from a backup file and assign access permissions.
- A user with the " **public**" role, whose permissions are limited. You will need this user to set up a secure connection to the restored Creatio database using PostgreSQL authentication.

If your PostgreSQL instance already has sysadmin (privileged) and public (unprivileged) user roles, skip this step.

To create PostgreSQL users:

01. Log in as **postgres**:





    ```cli
    sudo su - postgres
    ```

02. Open PostgreSQL shell:





    ```cli
    psql
    ```

03. Create a sysadmin user:





    ```sql
    CREATE USER pg_sysadmin;
    ```









    **pg\_sysadmin** – user who will be granted sysadmin privileges. This user will restore the Creatio database from a backup file and assign access permissions

04. Make **pg\_sysadmin** a system administrator:





    ```sql
    ALTER ROLE pg_sysadmin WITH SUPERUSER;
    ```

05. Allow **pg\_sysadmin** to log in:





    ```sql
    ALTER ROLE pg_sysadmin WITH LOGIN;
    ```

06. Set a password for **pg\_sysadmin**:





    ```sql
    ALTER ROLE pg_sysadmin WITH PASSWORD 'pg_syspassword';
    ```









    **pg\_password** – sysadmin user password for connecting to the PostgreSQL server.

07. Create a public user:





    ```sql
    CREATE USER pg_user;
    ```









    **pg\_user** – public user for connecting to the PostgreSQL server. You will need this user to set up a connection to the restored Creatio database.

08. Allow **pg\_user** to log in:





    ```sql
    ALTER ROLE pg_user WITH LOGIN;
    ```

09. Set a password for **pg\_user**:





    ```sql
    ALTER ROLE pg_user WITH PASSWORD 'pg_password';
    ```









    **pg\_password** – public user password for connecting to the PostgreSQL server.

10. Exit the PostgreSQL shell:


```cli
\q
```

11. Log out from your postgres session:

```cli
exit
```

## III. Restore PostgreSQL database [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux\#title-250-3 "Direct link to III. Restore PostgreSQL database")

To restore a PostgreSQL database from a backup file, you will need **psql** and **pg\_restore** utilities. Both are part of the **postgresql-client-common** package.

If you install **postgresql-12** locally using **apt-get**, APT will install **postgresql-client-common** as a dependency for **postgresql-12**.

If you plan to use a remote PostgreSQL database without installing the PostgreSQL DBMS on your server, install the **postgresql-client-common** package manually by running:

```cli
sudo apt-get install postgresql-client-common
```

To restore the Creatio database from a backup file:

1. Enter DB connection password in the environment variable:





```cli
export PGPASSWORD=pg_syspassword
```









**pg\_syspassword** – pg\_sysadmin user password for connecting to the PostgreSQL server.

2. Create a database where the backup data will be restored:





```cli
psql --host=pg_server_address --port=pg_server_port --username=pg_sysadmin --dbname=pg_dbname -c "CREATE DATABASE pg_dbname_creatio WITH OWNER = pg_user ENCODING = 'UTF8' CONNECTION LIMIT = -1"
```









**pg\_server\_address** – PostgreSQL server address

**pg\_server\_port** – PostgreSQL server port

**pg\_sysadmin** – sysadmin user for connecting to the PostgreSQL server

**pg\_dbname** – name of the PostgreSQL DB where the instructions will be executed



note





If you have not created any databases yet or an attempt to connect to a database triggers the "FATAL: database "pg\_dbname" does not exist" error, use the default database "template1".





**pg\_dbname\_creatio** – name of the PostgreSQL DB which will host Creatio tables

**pg\_user** – the "public" user who will be granted permission to use and update the Creatio database

3. If you are using AWS RDS:
1. Download the [ChangeTypesOwner.sql](https://academy.creatio.com/sites/default/files/documents/downloads/ChangeTypesOwner.sql) script.
2. In the script, replace the "postgres" value with a valid Postgres username.
3. Run the updated ChangeTypesOwner.sql script.
4. Navigate to the application directory:





```cli
cd /path/to/application/directory/
```









**/path/to/application/directory/** – the directory with Creatio setup files.

5. Navigate to the database directory:





```cli
cd db
```

6. Restore the database from the backup file:





```cli
pg_restore --host pg_server_ip --port pg_server_port --username=pg_sysadmin --dbname=pg_dbname_creatio --no-owner --no-privileges --verbose \path\to\db.backup
```









**pg\_server\_address** – PostgreSQL server address

**pg\_server\_port** – PostgreSQL server port

**pg\_sysadmin** – sysadmin user for connecting to the PostgreSQL server

**pg\_dbname\_creatio** – name of the PostgreSQL DB to insert backup tables. Use the name you specified in the "CREATE DATABASE" command on step 2.

7. Download the [CreateTypeCastsPostgreSql.sql file](https://academy.creatio.com/sites/default/files/documents/downloads/CreateTypeCastsPostgreSql.sql).

8. Execute type conversion:





```cli
psql --host=pg_server_address --port=pg_server_port --username=pg_sysadmin --dbname=pg_dbname_creatio --file=/path/to/CreateTypeCastsPostgreSql.sql
```









**pg\_server\_ip** – PostgreSQL server address

**pg\_server\_port** – PostgreSQL server port

**pg\_sysadmin** – sysadmin user for connecting to the PostgreSQL server

**pg\_dbname\_creatio** – name of the PostgreSQL DB where the instructions will be executed

**/path/to/CreateTypeCastsPostgreSql.sql** – path to the CreateTypeCastsPostgreSql.sql file.


## IV. Configure max connections (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux\#title-2500-7 "Direct link to IV. Configure max connections (optional)")

Important

Take these steps only if your Creatio deployment is going to serve more than 100 simultaneous users.

To configure max connections, set up the following parameters:

- **max\_connections** in the postgresql.conf file
- **shared\_buffers** in the postgresql.conf file
- **kernel.shmmax** in the /etc/sysctl.conf file

Run the following command to find the path to the postgresql.conf file:

```sql
SHOW config_file
```

1. Set **max\_connections** parameter based on the expected number of simultaneous users. Calculate the parameter value using the following formula:





```text
Expected number of users * 1.5
```









If the result is less or equals 1024, use the resulting number. If the result is more or equals 1024, set the parameter to 1024.

2. Set **shared\_buffers** based on the **max\_connections** value. Calculate the parameter value using the following formula:





```text
max_connections * 0.24MB
```









Set the parameter value to MB and round the resulting value up. For example, if **max\_connections** is 1024, **shared\_buffers** is 245,76MB rounded up, i.e., 246MB.

3. Set **kernel.shmmax** based on the **shared\_buffers** value. Calculate the parameter value using the following formula:





```text
shared_buffers + 16MB
```









Convert the resulting value to bytes. For example, if **shared\_buffers** is 246MB, **kernel.shmmax** is 274 726 912.


## V. Change the database owner (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux\#title-2500-6 "Direct link to V. Change the database owner (optional)")

Creatio lets you replace the owner of the database and its objects to a non-administrator user (not a superuser) during the restoration. Use the ChangeDbObjectsOwner script for that. For Postgres version 10 and earlier: [Download the script](https://academy.creatio.com/sites/default/files/documents/downloads/ChangeDbObjectsOwner.sql). For Postgres version 11 and later: [Download the script](https://academy.creatio.com/sites/default/files/documents/downloads/ChangeDbObjectsOwner_Postgres11.v2.sql).

To restore the database on behalf of a non-administrator user:

1. Replace the database owner:





```cli
psql --host pg_server_address --port pg_server_port --username=pg_sysadmin --dbname=pg_dbname –-command "ALTER DATABASE pg_dbname_creatio OWNER TO pg_user"
```









**pg\_server\_address** – PostgreSQL server address

**pg\_server\_port** – PostgreSQL server port

**pg\_sysadmin** – sysadmin user for connecting to the PostgreSQL server This user must be an administrator (superuser) or have the "ALTER DATABASE" privileges.

**pg\_user** – the placeholder to replace with the actual username of the new database owner. You will need this user to set up a connection to the Creatio database.

**pg\_dbname\_creatio** – the name of the database whose owner is being changed.

2. Replace the owner of the database objects:





```cli
psql --host pg_server_address --port pg_server_port --username=pg_sysadmin --dbname=pg_dbname_creatio --file=/path/toChangeDbObjectsOwner.sql --variable owner=pg_user --variable ON_ERROR_STOP=1
```









**pg\_server\_address** – PostgreSQL server address

**pg\_server\_port** – PostgreSQL server port

**pg\_sysadmin** – sysadmin user for connecting to the PostgreSQL server This user must be an administrator (superuser) or the Creatio database owner

**pg\_user** – the placeholder to replace with the actual username of the new database owner. You will need this user to set up a connection to the Creatio database.

**pg\_dbname\_creatio** – the name of the database whose owner is being changed.

**/path/toChangeDbObjectsOwner.sql** – the path to the previously saved toChangeDbObjectsOwner.sql file.


You can ignore this step. In that case, the user who ran the pg\_restore command will remain the owner of the database and its objects. Normally, this is the postgres user.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux\#see-also "Direct link to See also")

[Set up Creatio caching server](https://academy.creatio.com/documents?product=administration&ver=7&id=2135)

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?product=administration&ver=7&id=2136)

[Creatio setup FAQ](https://academy.creatio.com/documents?product=administration&ver=7&id=1634)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [I. Install PostgreSQL](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux#title-250-1)
- [II. Create PostgreSQL user](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux#title-250-2)
- [III. Restore PostgreSQL database](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux#title-250-3)
- [IV. Configure max connections (optional)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux#title-2500-7)
- [V. Change the database owner (optional)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux#title-2500-6)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/database-server/deploy-postgresql-database-linux#see-also)