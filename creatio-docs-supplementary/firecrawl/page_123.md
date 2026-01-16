<!-- Source: page_123 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)** (8.3).

Version: 8.0All Creatio products

On this page

Use one of two database configurations to deploy Creatio:

- Use a remote DBMS (recommended)
- Use a local PostgreSQL server.

If you already have a PostgreSQL server set up, skip to step II.

If you have already set up sysadmin (with privileges to log in, create and modify databases) and public (unprivileged) user roles, skip to step III.

## I. Install PostgreSQL [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows\#title-251-1 "Direct link to I. Install PostgreSQL")

PostgreSQL setup files are available for download at [postgresql.org](https://www.postgresql.org/download/).

note

High-availability PostgreSQL configurations have not been tested with Creatio. Please refer to the [PostgreSQL documentation](https://www.postgresql.org/docs/9.5/high-availability.html) for details on PostgreSQL clustering.

## II. Create PostgreSQL user [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows\#title-251-2 "Direct link to II. Create PostgreSQL user")

A fresh installation of PostgreSQL Server is not ready for deploying Creatio immediately. If you plan to use a fresh installation of PostgreSQL Server, you need to create a user that can log in to the database using a password and has sufficient privileges to create and update a database. By default, no such user will be available.

We recommend to create two database users in PostgreSQL:

- A user with the " **sysadmin**" role who has maximum access privileges on the database server level. This user will restore the Creatio database from a backup file and assign access permissions. These instructions use **pg\_sysadmin** as a placeholder username, but you can set the username to any value.
- A user with the " **public**" role whose permissions are limited. You will need this user to set up a secure connection to the restored Creatio database using PostgreSQL authentication. These instructions use **pg\_user** as a placeholder username, but you can set the username to any value.

To create the two PostgreSQL users:

01. Open the Command Prompt.

02. Navigate to the PostgreSQL software install folder:





    ```cli
    cd /D "\path\to\PostgreSQL\folder"
    ```









    **\\path\\to\\PostgreSQL\\folder** – the path to the PostgreSQL software install folder.

03. Navigate to the folder with the Command Line Tools component:





    ```cli
    cd bin
    ```

04. Enter the DB connection password in the environment variable.





    ```cli
    set PGPASSWORD=pg_password
    ```









    **pg\_password** – password of the **postgres** user for connecting to the PostgreSQL server.

05. Run PostgreSQL shell as **postgres**:





    ```cli
    psql.exe --username postgres
    ```

06. Create a sysadmin user, e. g. **pg\_sysadmin**:





    ```sql
    CREATE USER pg_sysadmin;
    ```









    **pg\_sysadmin** – placeholder name for a sysadmin user. The sysadmin will restore the Creatio database from a backup file and assign access permissions.

07. Make **pg\_sysadmin** a system administrator:





    ```sql
    ALTER ROLE pg_sysadmin WITH SUPERUSER;
    ```

08. Allow **pg\_sysadmin** to log in:





    ```sql
    ALTER ROLE pg_sysadmin WITH LOGIN;
    ```

09. Set a password for **pg\_sysadmin**:





    ```sql
    ALTER ROLE pg_sysadmin WITH PASSWORD 'pg_syspassword';
    ```









    **pg\_syspassword** – sysadmin user password for connecting to the PostgreSQL server.

10. Create a public user, e. g. **pg\_user**:





    ```sql
    CREATE USER pg_user;
    ```









    **pg\_user** – placeholder name for a public user. This user will set up a connection to the restored Creatio database.

11. Allow **pg\_user** to log in:


```sql
ALTER ROLE pg_user WITH LOGIN;
```

12. Set a password for **pg\_user**:





    ```sql
    ALTER ROLE pg_user WITH PASSWORD 'pg_password';
    ```









    **pg\_password** – public user password for connecting to the PostgreSQL server.

13. Exit the PostgreSQL shell:





    ```cli
    \q
    ```


## III. Restore PostgreSQL database [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows\#title-251-3 "Direct link to III. Restore PostgreSQL database")

To restore a PostgreSQL database from a backup file, you will need **psql.exe** and **pg\_restore.exe** utilities. Both are part of the Command Line Tools PostgreSQL component that comes with the PostgreSQL Server. They are located in the PostgreSQL software install folder.

If you plan to use a remote PostgreSQL database without installing the PostgreSQL Server on your machine, take the following steps:

1. Get a PostgreSQL binary package. Binary packages are available for download at [postgresql.org](https://www.postgresql.org/download/).
2. Select the Command Line Tools component during installation. Selecting the other components is optional.

To restore the Creatio database from a backup file:

01. Open Command Prompt.

02. Navigate to the PostgreSQL software install folder:





    ```cli
    cd /D "\path\to\PostgreSQL\folder"
    ```









    **\\path\\to\\PostgreSQL\\folder** – the path to the PostgreSQL software install folder.

03. Navigate to the folder with executables:





    ```cli
    cd bin
    ```

04. Enter the DB connection password in the environment variable:





    ```cli
    set PGPASSWORD=pg_syspassword
    ```









    **pg\_syspassword** – sysadmin user password for connecting to the PostgreSQL server.

05. Create a database where the backup data will be restored.





    ```cli
    psql.exe --host pg_server_ip --port pg_server_port --username=pg_sysadmin --command "CREATE DATABASE pg_dbname_creatio WITH OWNER = pg_user ENCODING = 'UTF8' CONNECTION LIMIT = -1"
    ```









    **pg\_server\_ip** – PostgreSQL server address.

    **pg\_server\_port** – PostgreSQL server port.

    **pg\_sysadmin** – user for connecting to the PostgreSQL server. The user must have either superuser (administrator) privileges or "CREATE DATABASE" privileges

    **pg\_user** – the application will use this user's credentials to connect to the database. You can specify any user when creating the database. To change the user data, follow **step 10** of this instruction.

06. If you are using AWS RDS:
    1. Download the [ChangeTypesOwner.sql](https://academy.creatio.com/sites/default/files/documents/downloads/ChangeTypesOwner.sql) script.
    2. In the script, replace the "postgres" value with a valid Postgres username.
    3. Run the updated ChangeTypesOwner.sql script.
07. Restore the Creatio database from the backup file:





    ```cli
    pg_restore --host pg_server_ip --port pg_server_port --username=pg_sysadmin --dbname=pg_dbname_creatio --no-owner --no-privileges --verbose \path\to\db.backup
    ```









    **pg\_server\_ip** – PostgreSQL server address.

    **pg\_server\_port** – PostgreSQL server port.

    **pg\_sysadmin** – user for connecting to the PostgreSQL server. The user must have either superuser (administrator) privileges or sufficient access permissions to run the **pg\_restore** utility.

    **pg\_dbname\_creatio** – name of the PostgreSQL DB to insert backup tables.

08. Download the [CreateTypeCastsPostgreSql.sql file](https://academy.creatio.com/sites/default/files/documents/downloads/CreateTypeCastsPostgreSql.sql).

09. Execute type conversion:





    ```cli
    psql.exe --host pg_server_ip --port pg_server_port --username=pg_sysadmin --dbname=pg_dbname_creatio --file=\path\to\CreateTypeCastsPostgreSql.sql
    ```









    **pg\_server\_ip** – PostgreSQL server address.

    **pg\_server\_port** – PostgreSQL server port.

    **pg\_sysadmin** – user with administrator privileges for connecting to the PostgreSQL server.

    **pg\_dbname\_creatio** – name of the PostgreSQL DB where the instructions will be executed.

    **\\path\\to\\CreateTypeCastsPostgreSql.sql** – path to the downloaded CreateTypeCastsPostgreSql.sql file.

10. Creatio version **7.16.3** supports changing the owner of the database and database objects to a non-administrator user (i. e., not a superuser). To do this, use the ChangeDbObjectsOwner script. [Download the script](https://academy.creatio.com/sites/default/files/documents/downloads/ChangeDbObjectsOwner.sql).

    To restore the database from a backup as a regular user:


    1. Change the owner of the database:

```cli
psql.exe --host pg_server_ip --port pg_server_port --username=pg_sysadmin --dbname=pg_dbname –-command "ALTER DATABASE pg_dbname_creatio OWNER TO pg_user"
```

    - **pg\_server\_ip**: PostgreSQL server address.

    - **pg\_server\_port**: PostgreSQL server port.

    - **pg\_sysadmin**: user for connecting to the PostgreSQL server. The user must have either administrator (superuser) privileges or "CREATE DATABASE" privileges.

    - **pg\_user**: new database owner.

    - **pg\_dbname\_creatio**: the name of the database whose owner is changed.


    2. Change the owner of the database objects:

```cli
psql.exe --host pg_server_ip --port pg_server_port --username=pg_sysadmin --dbname=pg_dbname_creatio --file=\\path\to\ChangeDbObjectsOwner.sql --variable owner=pg_user --variable ON_ERROR_STOP=1
```

    - **pg\_server\_ip**: PostgreSQL server address.
    - **pg\_server\_port**: PostgreSQL server port.
    - **pg\_sysadmin**: user for connecting to the PostgreSQL server. The user must have either administrator (superuser) privileges or "CREATE DATABASE" privileges.
    - **pg\_user**: new database owner.
    - **pg\_dbname\_creatio**: the name of the database whose owner is changed.
    - **\\path\\to\\ChangeDbObjectsOwner.sql**: path to the downloaded ChangeDbObjectsOwner.sql file.

Skip this step to leave the default owner of the database and database objects, which is the user who runs the **pg\_restore** utility (usually **postgres**)

## IV. Configure max connections (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows\#title-251-4 "Direct link to IV. Configure max connections (optional)")

Important

Take these steps only if your Creatio deployment is going to serve more than 100 simultaneous users.

To configure max connections, set up the following parameters:

- **max\_connections** in the postgresql.conf file
- **shared\_buffers** in the postgresql.conf file

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


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows\#see-also "Direct link to See also")

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?product=administration&ver=7&id=2136)

[Creatio setup FAQ](https://academy.creatio.com/documents?product=administration&ver=7&id=1634)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

- [I. Install PostgreSQL](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows#title-251-1)
- [II. Create PostgreSQL user](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows#title-251-2)
- [III. Restore PostgreSQL database](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows#title-251-3)
- [IV. Configure max connections (optional)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows#title-251-4)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/on-site-deployment/database_server/deploy_postgresql_database_windows#see-also)