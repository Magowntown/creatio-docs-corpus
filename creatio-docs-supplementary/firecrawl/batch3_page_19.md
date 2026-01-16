<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/oauth-health-monitoring#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3On-site

On this page

Use the functionality to discover what goes wrong during the Identity Service or OAuth setup and usage. You can use the functionality manually or as part of integration with automated monitoring systems.

note

This functionality is available for Creatio deployed on .NET Framework only.

OAuth health check functionality checks whether:

- the system settings that configure OAuth 2.0 in Creatio are filled out
- the Identity service is available
- the OAuth access token is retrievable

To **check the health of OAuth functionality from the browser**, use the following link:

- For .NET Framework: `http://mycreatio.com/0/api/OAuthHealthCheck`
- For .NET: `http://mycreatio.com/api/OAuthHealthCheck`

**As a result**, you will receive one of the responses listed below.

Response

```js
Status: 200 OK

{
    "HasProblem": false,
    "IsSystemSettingsFilledIn": true,
    "IsIdentityServiceAvailable": true,
    "IsAccessTokenRetrievableForSystemActions": true
}
```

OAuth access token is received from the Identity Service as expected.

**Solution**. Not required.

* * *

Response

```js
Status: 500 Internal Server Error

{
    "HasProblem": true,
    "IsSystemSettingsFilledIn": false,
    "IsIdentityServiceAvailable": false,
    "IsAccessTokenRetrievableForSystemActions": false,
    "Message": "System settings OAuth20IdentityServerUrl, OAuth20IdentityServerClientId, OAuth20IdentityServerClientSecret are empty."
}
```

The system settings that configure OAuth 2.0 in Creatio are not filled out.

**Solution**. Make sure that the following system settings are filled out:

- "Authorization server Url for OAuth 2.0 integrations" (`OAuth20IdentityServerUrl` code)
- "Client id for OAuth 2.0 integrations" (`OAuth20IdentityServerClientId` code)
- "Client secret for OAuth 2.0 integrations" (`OAuth20IdentityServerClientSecret` code)

* * *

Response

```js
Status: 500 Internal Server Error

{
    "HasProblem": true,
    "IsSystemSettingsFilledIn": false,
    "IsIdentityServiceAvailable": false,
    "IsAccessTokenRetrievableForSystemActions": false,
    "Message": "System setting OAuth20IdentityServerUrl is empty."
}
```

An individual system setting that configures OAuth 2.0 in Creatio is not filled out.

**Solution**.

1. Find the code of the system setting that causes error in the `Message` response parameter.
2. Fill out the needed system setting.

* * *

Response

```js
Status: 500 Internal Server Error

{
    "HasProblem": true,
    "IsSystemSettingsFilledIn": true,
    "IsIdentityServiceAvailable": false,
    "IsAccessTokenRetrievableForSystemActions": false,
    "Message": "IdentityService specified in system setting OAuth20IdentityServerUrl is unavailable."
}
```

Identity Service is not working as expected.

**Solution**. Test the Identity Service. Instructions: [Test the Identity Service](https://academy.creatio.com/documents?id=2396&anchor=title-2002-7). If **the Identity Service is available**, check that the "Authorization server Url for OAuth 2.0 integrations" (`OAuth20IdentityServerUrl` code) system setting is filled out and Identity Service URL is available from the machine where Creatio instance is deployed.

* * *

Response

```js
Status: 500 Internal Server Error

{
    "HasProblem": true,
    "IsSystemSettingsFilledIn": true,
    "IsIdentityServiceAvailable": true,
    "IsAccessTokenRetrievableForSystemActions": false,
    "Message": "Can't retrieve access_token for system actions from IdentityService specified in system settings OAuth20IdentityServerUrl using client_id and client_secret specified in system settings OAuth20IdentityServerClientId & OAuth20IdentityServerClientSecret."
}
```

OAuth access token is not available.

**Solution**.

1. Make sure that the following system settings are filled out:
   - "Authorization server Url for OAuth 2.0 integrations" (`OAuth20IdentityServerUrl` code)
   - "Client id for OAuth 2.0 integrations" (`OAuth20IdentityServerClientId` code)
   - "Client secret for OAuth 2.0 integrations" (`OAuth20IdentityServerClientSecret` code)
2. If system settings are filled out, reproduce the issue and collect Creatio and Identity Service logs that include data when the issue occurred.

3. Contact [Creatio support](mailto:support@creatio.com) and provide them Creatio and Identity Service logs.


You can **set up automated monitoring systems** based on OAuth health monitoring. If needed, use **Postman** to check the health of OAuth functionality. The Postman request collection that tests requests is available in [Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest#0e2dd1ce-1a5d-4870-bb0b-c0cc2eb25a31).

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/oauth-health-monitoring\#see-also "Direct link to See also")

[Deploy the Identity Service](https://academy.creatio.com/documents?id=2466)

[Connect the Identity Service to Creatio](https://academy.creatio.com/documents?id=2467)

[Set up client credentials grant](https://academy.creatio.com/documents?id=2508)

[Set up authorization code grant](https://academy.creatio.com/documents?id=2576)

[Update the Identity Service using IIS](https://academy.creatio.com/documents?id=2468)

[Authorize external requests using client credentials grant (developer documentation)](https://academy.creatio.com/documents?id=15058)

[Authorize external requests using authorization code grant (developer documentation)](https://academy.creatio.com/documents?id=15188)

* * *

## Resources [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/oauth-health-monitoring\#resources "Direct link to Resources")

[Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest)

- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/oauth-health-monitoring#see-also)
- [Resources](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/oauth-health-monitoring#resources)