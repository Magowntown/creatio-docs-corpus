<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/administration/security-settings/store-secrets-in-vault)** (8.3).

Version: 8.1

On this page

You can improve security of Creatio by not storing sensitive data in the configuration files. Use [Vault by HashiCorp](https://www.vaultproject.io/) designed for secure storage and management of sensitive data. Sensitive data include:

- passwords
- usernames
- API keys
- access tokens

You can use a secure Vault storage for your connection parameters normally stored in the ConnectionStrings.config file:

- Creatio databases
- Quartz (if stored in a separate DB)
- Redis
- s3Connection
- ElasticSearch
- influx
- MessageBroker

You can move the connection parameters to Vault during [deployment](https://academy.creatio.com/docs/8.x/setup-and-administration/category/on-site-deployment) or in a deployed environment.

Vault uses secrets to store sensitive data. Secrets are written to Secrets Engines: storages of secrets. There are several types of Secrets Engines. Use the key-value (KV version 2) Secrets Engine type for the storage of sensitive Creatio data. This will enable you to store sensitive information as key-value pairs. The value is the sensitive information, while the key must be specified in the ConnectionString.config file of your Creatio server. You can also store encryption keys (AES) in Vault.

note

You can further configure Vault to track versioned key-value pairs.

Fig. 1 Interaction diagram for Creatio and Vault

![Fig. 1 Interaction diagram for Creatio and Vault](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/vault/vault_creatio_scheme.png)

The general procedure for Vault connection and setup is as follows:

1. Steps on the Vault side:
1. Deploy and run the Vault server.
2. Create secret keys.
3. Set up the security policy.
4. Set up the authorization parameters.
2. Steps on the Creatio side:
1. Set up Vault connection parameters.
2. Set up the string in ConnectionString.config.
3. Enable the flags.
4. Restart Creatio.

Let’s consider these steps in more detail.

## Steps on the Vault side [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-21 "Direct link to Steps on the Vault side")

### Deploy and run the Vault server [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-1 "Direct link to Deploy and run the Vault server")

Run the Vault server in production mode before use. You can deploy Vault both on a dedicated server and a server with other Creatio components, guided by the general [server-side system requirements](https://academy.creatio.com/documents?id=1456). This can be done during the deployment of Creatio or at a later stage.

Deploy the Vault server on a Linux/Windows machine and enable HTTPS. Use the server certificate stored on the same machine as the Vault server to configure HTTPS. The certificate can be issued and signed by any trusted CA.

Important

Store the private key for the server certificate in a protected directory.

The Vault documentation covers deployment and launch in more detail:

1. [Installation](https://learn.hashicorp.com/tutorials/vault/getting-started-install).
2. [Configuration](https://learn.hashicorp.com/tutorials/vault/configure-vault).
3. First [start](https://www.vaultproject.io/docs/commands/server).
4. [Initialization](https://www.vaultproject.io/docs/commands/operator/init) after the first start.

note

Save the unseal keys and token generated during the initialization. This is required to ensure starting the server is safe and start it with administrator privileges.

Actions performed each time the Vault server is restarted:

1. [Restart](https://www.vaultproject.io/docs/commands/server).
2. [Unsealing](https://www.vaultproject.io/docs/concepts/seal) using the unseal keys generated during the initialization.

### Create a storage for secret keys [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-2 "Direct link to Create a storage for secret keys")

Use the key-value (KV version 2) Secrets Engine for the storage of secrets.

Vault can store versioned sensitive data in specialized storages (Secrets Engines). Each secrets engine has a unique path as an attribute required for connection. We recommend using your website’s name as the path for the storage of sensitive Creatio data.

1. Go to the **Secrets** section in the Vault UI.
2. Create a key-value secrets engine. We recommend using the name of the product for which the secrets are created as the name of the secrets engine. For example, Creatio. Learn more about creating a secrets engine in the [Vault documentation](https://www.vaultproject.io/docs/secrets/kv/kv-v2).

A secrets engine can hold several secrets, each corresponding to a specific connection string or encryption key. Specify a unique path to each secret in the secrets engine. A single secret can hold multiple key-value pairs, each pair meant for a different type of sensitive data. For example, a login and its password are stored in Vault as two key-value pairs,

### Create secret keys [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-3 "Direct link to Create secret keys")

To create private keys for the database connection string in the ConnectionString.config file:

1. Go to the **Secrets** section in the Vault UI.

2. Open the secrets engine you created.

3. Specify the Path to the secret. To connect to the database, as well as to Redis, the path to sensitive data must match the name of the corresponding connection string in ConnectionStrings.config. For example, if you are using PostgreSql, specify dbPostgreSql in the database connection string.

4. Configure other connection strings that contain sensitive data in the same way.

5. In each secret that has a matching connection string, create all required key-value pairs where the key contains a unique secret name (we recommend meaningful names so that the key is easy to identify) and the value contains the sensitive data. Keys and values ​​are case-sensitive.

As a result, the path to the created secret is as follows: `<secretsEnginePath>/dbPostgreSql`, where `<secretsEnginePath>` is the path to the secrets engine, and dbPostgreSql is the path to the secret.



Important





When changing secret values in Vault, restart Creatio to use the new values.


Fig. 2 An example of filled-in keys in Vault

![Fig. 2 An example of filled-in keys in Vault](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/vault/vault_keys.png)

This example uses the data from the following line in the ConnectionStrings.config file:

```xml
<add name="dbPostgreSql" connectionString="Pooling=true; Database=SOME_DB_NAME; Host=SOME_DB_HOST; Username=SOME_USER; Password=SOME_PASSWORD; Port=SOME_DB_PORT; Timeout=5; CommandTimeout=400" />
```

where:

- DbHost is the DB server address that matches the Host parameter with the value of SOME\_DB\_HOST.
- DbPort is the DB server port that matches the Port parameter with the value of SOME\_DB\_PORT.
- DbName is the DB server name that matches the Database parameter with the value of SOME\_DB\_NAME.
- Username is the DB username that matches the Username parameter with the value of SOME\_USER.
- Password is the DB password that matches the Password parameter with the value of SOME\_PASSWORD.

Learn more: [Versioned Key/Value Secrets Engine](https://learn.hashicorp.com/tutorials/vault/versioned-kv) (official Vault documentation).

### Set up the security policy [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-5 "Direct link to Set up the security policy")

Since Vault can store different types of sensitive information, we recommend creating separate security policies to control the access levels for the specified keys. Creatio’s access privileges to the secrets engine must be read-only.

In the future, you can use these policies when generating authorization client tokens or when adding client certificates to Vault.

A policy that gives Creatio read access to all secrets in the secrets engine with the `<secretsEnginePath>` path is as follows:

```xml
path "<secretsEnginePath>/*" {capabilities = ["read", "list"] }
```

where `<secretsEnginePath>` is the path to the [secrets engine](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-2).

Learn more: [Policies](https://www.vaultproject.io/docs/concepts/policies) (official Vault documentation).

### Set up Vault authorization [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-6 "Direct link to Set up Vault authorization")

Creatio supports the following Vault authorization types:

- by client certificate
- by token.

#### Set up certificate authorization [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-7 "Direct link to Set up certificate authorization")

1. Issue a sseparate [client certificate](https://www.vaultproject.io/docs/auth/cert) and register it on the Creatio host machine.
2. Add the certificate to Vault as the authorization method.
3. Specify the [policy](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-5) to read the secrets with the data from the connection strings.

Learn more: [Auth Methods](https://www.vaultproject.io/docs/auth) (official Vault documentation).

#### Set up token authorization [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-8 "Direct link to Set up token authorization")

Vault generates a Root Token upon initialization. We strongly advise against using that token for authorization as it grants virtually unlimited privileges. For Creatio authorization, generate a client token with security policies that would only allow to read secrets meant to substitute the templates in the connection strings of your application.

To generate a client token for Creation authorization in Vault, run the following command:

```cli
vault token create -policy=<policyName>
```

where `<policyName>` is the name of the [security policy](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-5).

Learn more: [Tokens](https://www.vaultproject.io/docs/concepts/tokens), [Token create - Command](https://www.vaultproject.io/docs/commands/token/create) (official Vault documentation).

## Settings on the Creatio side [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-9 "Direct link to Settings on the Creatio side")

### Set up Vault connection parameters [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-17 "Direct link to Set up Vault connection parameters")

Vault connection settings must be specified in the vaultConfig section of the **web.config** file in the Creatio root folder. The parameters of the section are described in the table below:

| Parameter name | Details | Value |
| --- | --- | --- |
| hostUri | A string with the address of the Vault server | The pattern: `https://<Vault server address>:<Vault server port>`. |
| authMethodType | Authorization type | Acceptable values: **Token**. Authorize by token. **Cert**. Authorize by certificate. |
| secretsEnginePath | The path to the Vault secrets engine | We recommend using your website’s name as the value. |
| token | A string with the client token. | Specified if authorizing by token. |
| certFilePath | Path to the certificate. Creatio version 8.0.5 Atlas and later lets you store Vault authentication certificates in Windows Certificate Store. Also, the certificate can now be read both by the name and ThumbPrint. | Specified if authorizing by certificate. |
| certPassword | The password for the certificate. | Specified if the certificate is password-protected, blank otherwise. |

If an illegal value if specified as authMethodType, Creatio will throw an error.

- Token connection example
- Certificate connection example

```xml
<vaultConfig hostUri="https://127.0.0.1:1024" authMethodType="Token" token="s.on3zJH6fXZlodRAYqgTXYEot" secretsEnginePath="<secretsEnginePath>" />
```

```xml
<vaultConfig hostUri="https://127.0.0.1:1024" authMethodType="Cert" certFilePath="<path>" certPassword="<password>" secretsEnginePath="<secretsEnginePath>" />
```

where

- `<secretsEnginePath>` is the path to the secrets engine
- `<path>` is the path to the certificate file
- `<password>` is the password to unlock the certificate file.

### Set up connection string templates [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-18 "Direct link to Set up connection string templates")

The ConnectionStrings.config file must contain connection string templates for substitution with Vault secrets. Build templates by using the secret keys’ names enclosed in **brackets** instead of the secret values.

For example, if a connection string has a Password="somePassword" value, its template must reference it as Password="\[DBPassword\]", where DBPassword is the secret key’s name in Vault.

If a connection string has no secret data, leave it unchanged. In that case, the value of the string will not be substituted with its Vault counterpart.

For example, if the config file has the following connection string:

```xml
<add name="dbPostgreSql" connectionString="Pooling=true; Database=SOME_DB_NAME; Host=SOME_DB_HOST; Username=SOME_USER; Password=SOME_PASSWORD; Port=SOME_DB_PORT; Timeout=5; CommandTimeout=400" />
```

its template may look as follows:

```xml
<add name="dbPostgreSql" connectionString="Pooling=true; Database=[DbName]; Host=[DbHost]; Username=[Username]; Password=[Password]; Port=[DbPort]; Timeout=5; CommandTimeout=400" />
```

where DbHost, DbPort, DbName, Username, Password are the keys of the corresponding secrets stored in Vault.

### Enable flags [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-30 "Direct link to Enable flags")

To configure **connection strings** in the web.config file located in the Creatio root folder, add the following lines to the `<appSettings>` section:

```xml
<add key="UseConnectionStringProvider" value="true" />
<add key="UseSecretsInConnectionStrings" value="true" />
```

If you also want to use **encryption keys** (AES), take the following steps:

1. Add the `<appSettings>:<add key="UseSecretsInEncryptionKeys" value="true" />` line to the section in the web.config file located in the Creatio root folder.

2. In the Vault secrets storage whose name is specified in the configuration file in the vaultConfig section → the secretsEnginePath parameter, add a secret named EncryptionKeys.

3. In the EncryptionKeys secret, add the keys with the values ​​specified in the Creatio configuration file:
   - InitializationSecurityVector,
   - CurrentSecurityKey.
4. Remove the InitializationSecurityVector and CurrentSecurityKey attributes from the configuration file.


Fig. 3 Example of filled-in keys

![Fig. 3 Example of filled-in keys](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/vault/aes_keys.png)

Important

The names of the secret and keys must exactly match the ones above. If the flags are disabled, Vault will not correctly store sensitive data of Creatio.

Restart Creatio to apply the changes.

## Disable storage of keys in Vault [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#title-3786-20 "Direct link to Disable storage of keys in Vault")

To disable storage of AES keys in Vault, take the following steps:

1. Add the following flags to the configuration file of Creatio:


   - InitializationSecurityVector
   - CurrentSecurityKey.

The values ​​of the keys are stored in the Vault secrets engine whose name is specified in the configuration file in the vaultConfig section → the secretsEnginePath parameter → the EncryptionKeys secret:

```xml
<add key="InitializationSecurityVector" value="Vault_key_value" />
<add key="CurrentSecurityKey" value="Vault_key_value" />
```

2. Disable the UseSecretsInEncryptionKeys flag in the Creatio configuration file:





```xml
<add key="UseSecretsInEncryptionKeys" value="false" />
```

3. Restart Creatio to apply the changes.


* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault\#see-also "Direct link to See also")

[Modify ConnectionStrings.config for MS SQL Server](https://academy.creatio.com/documents?id=2138)

[Modify ConnectionStrings.config for Oracle Database](https://academy.creatio.com/documents?id=2139)

[Modify ConnectionStrings.config for PostgreSQL](https://academy.creatio.com/documents?id=2140)

[Prepare to deploy Creatio .NET Core on Linux](https://academy.creatio.com/documents?id=2120)

- [Steps on the Vault side](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-21)
  - [Deploy and run the Vault server](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-1)
  - [Create a storage for secret keys](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-2)
  - [Create secret keys](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-3)
  - [Set up the security policy](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-5)
  - [Set up Vault authorization](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-6)
- [Settings on the Creatio side](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-9)
  - [Set up Vault connection parameters](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-17)
  - [Set up connection string templates](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-18)
  - [Enable flags](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-30)
- [Disable storage of keys in Vault](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#title-3786-20)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/security-settings/store-secrets-in-vault#see-also)