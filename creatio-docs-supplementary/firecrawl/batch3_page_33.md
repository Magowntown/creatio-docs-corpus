<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3On-site

On this page

OpenSSL is an open-source toolkit that is widely used for implementing the SSL/TLS protocols, which are the standards for secure communication over computer networks. A **PFX certificate** is a digital document that verifies the identity of a website or server. Creatio uses it to sign access tokens that are issued by Identity Service, ensuring that your data is secure.

Each Identity Service instance should utilize a unique PFX certificate. The use of identical certificates across multiple environments constitutes a significant security vulnerability.

You can use a certificate that was issued by the certificate authority or a manually generated certificate. To generate a certificate manually, use the instructions below. The script that generates the PFX certificate is located in the archive with the Identity Service installation files.

Important

OAuth and OpenID authorization functionality support certificates encrypted with RSA, or ECDSA using the following combinations: P-256 with SHA-256, P-384 with SHA-384, or P-521 with SHA-512. When using certificates from a certificate authority, ensure they are signed with a supported encryption type to guarantee compatibility.

## General procedure [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-1 "Direct link to General procedure")

### Generate PFX certificate for Windows [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-1 "Direct link to Generate PFX certificate for Windows")

#### 1\. Install OpenSSL [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-2 "Direct link to 1. Install OpenSSL")

Install OpenSSL if needed. [Download the install file](https://wiki.openssl.org/index.php/Binaries).

The installation instructions are provided by the installer.

#### 2\. Set permissions to run PowerShell scripts [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-3 "Direct link to 2. Set permissions to run PowerShell scripts")

1. **Open PowerShell terminal as administrator**. To do this, right-click on the PowerShell icon and select "Run as administrator."

2. **Allow script execution**.
1. Run the following command at the PowerShell terminal: `Set-ExecutionPolicy RemoteSigned`.
2. Press Enter.
3. **Confirm the change** when prompted.


#### 3\. Generate the certificate [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-4 "Direct link to 3. Generate the certificate")

1. **Open PowerShell terminal**.

2. **Go to the script directory**. To do this, run the following command at the PowerShell terminal:





```cli
cd <rootIdentityServiceDirectory>\pfx\win
```









where `<rootIdentityServiceDirectory>` is the path to the root directory of the Identity Service.

3. **Execute the \*.ps1 script** using the following parameters:





```cli
.\generate_pfx.ps1 -pemPassword "YourSecurePassword" -outputPath "certificateDirectory" -validDays 365
```









where:
   - `YourSecurePassword` is the secure password for the PEM file. Make sure the password follows the recommendations.
     Password recommendations for PEM file







     - Use a strong password that has at least 12 characters.
     - Include a mix of uppercase and lowercase Latin letters, numbers, and special characters.
     - Avoid using common words or easily guessable patterns.
     - Store the password securely (e. g., in a password manager).

   - `certificateDirectory` is the desired output directory where you store the certificate. The default location for the certificate is the root directory of the Identity Service. If you want to keep certificate in the default location, set the parameter value to `"../../"`.

   - `365` is the desired validity period in days.

**As a result**, the script will generate an openssl.pfx certificate and save it to the specified output directory.

### Generate PFX certificate for Linux [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-6 "Direct link to Generate PFX certificate for Linux")

#### 1\. Install OpenSSL [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-7 "Direct link to 1. Install OpenSSL")

1. **Open the terminal**.

2. **Install OpenSSL** using package manager:
   - For Debian/Ubuntu: `sudo apt update && sudo apt install openssl -y`
   - For RHEL/CentOS: `sudo yum install openssl -y`
   - For Fedora: `sudo dnf install openssl -y`

#### 2\. Setup the bash script [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-8 "Direct link to 2. Setup the bash script")

To do this, run the following command:

```cli
chmod +x generate_pfx.sh
```

#### 3\. Generate the certificate [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-9 "Direct link to 3. Generate the certificate")

1. **Open the terminal**.

2. **Go to the script directory**. To do this, run the following command:





```cli
<rootIdentityServiceDirectory\pfx\linux\>
```









where `<rootIdentityServiceDirectory>` is the path to the root directory of the Identity Service.

3. **Execute the \*.ps1 script** with the following parameters:





```cli
./generate_pfx.sh "YourSecurePassword" "certificateDirectory" 365
```









where:
   - `YourSecurePassword` is the secure password for the PEM file. Make sure the password follows the recommendations.
     Password recommendations for PEM file







     - Use a strong password that has at least 12 characters.
     - Include a mix of uppercase and lowercase Latin letters, numbers, and special characters.
     - Avoid using common words or easily guessable patterns.
     - Store the password securely (e. g., in a password manager).

   - `certificateDirectory` is the desired output directory where you store the certificate. The default location for the certificate is the root directory of the Identity Service. If you want to keep certificate in the default location, set the parameter value to `"../../"`.

   - `365` is the desired validity period in days.

**As a result**, the script will generate an openssl.pfx certificate and save it to the specified output directory.

## Change PFX certificate in the existing Identity Service [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#title-2565-11 "Direct link to Change PFX certificate in the existing Identity Service")

Important

To prevent disruption and temporary service interruptions, we recommend changing PFX certificate in the existing Identity Service during non-business hours.

General recommendations:

- **Back up the existing openssl.pfx certificate**. Before replacing the existing certificate, create a backup to restore the previous version if necessary.
- **Test certificate replacement procedure on pre-production environment**. Thoroughly test the new certificate in a pre-production environment that is identical to the production environment. This lets you identify and resolve any potential issues before deploying to production.
- **Verify functionality**. After restarting the Identity Service and Creatio, carefully verify the proper functioning of OAuth 2.0 authorization in all integrations that utilize this method.

To change PFX certificate in the existing Identity Service:

1. **Add the openssl.pfx certificate into the existing Identity Service**.
1. Generate a new openssl.pfx certificate or copy an existing openssl.pfx certificate to your desired directory.
2. If needed, specify the full path to openssl.pfx certificate in the `X509CertificatePath` parameter of appsettings.json file in the root Identity Service directory.
2. **Restart Identity Service and Creatio** in one of the following ways:
   - using IIS







     1. Restart Identity Service.
        1. Open IIS Manager.
        2. Open the **Application Pools** section in the **Connections** area of the IIS.
        3. Go to the Identity Service application pool.
        4. Recycle the application pool. To do this, right-click on the Identity Service application pool → **Recycle**.
     2. Restart Creatio.
        1. Open IIS Manager.
        2. Open the **Application Pools** section in the **Connections** area of the IIS.
        3. Go to the Creatio application pool.
        4. Recycle the application pool. To do this, right-click on the Creatio application pool → **Recycle**.

   - using Docker







     1. Rebuild and restart the Identity Service container.
     2. Restart the Creatio app.

**As a result**, the PFX certificate in the existing Identity Service will be changed.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#see-also "Direct link to See also")

[Connect the Identity Service to Creatio](https://academy.creatio.com/documents?id=2467)

[Set up client credentials grant](https://academy.creatio.com/documents?id=2508)

[Set up authorization code grant](https://academy.creatio.com/documents?id=2576)

[OAuth health monitoring](https://academy.creatio.com/documents?id=2513)

[Authorize external requests using client credentials grant (developer documentation)](https://academy.creatio.com/documents?id=15058)

[Authorize external requests using authorization code grant (developer documentation)](https://academy.creatio.com/documents?id=15188)

[NLog (developer documentation)](https://academy.creatio.com/documents?id=15182)

* * *

## E-learning courses [​](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl\#e-learning-courses "Direct link to E-learning courses")

[Tech Hour - Integrate like a boss with Creatio, part 2 (Odata)](https://www.youtube.com/watch?v=ehjfcBxpLsQ)

- [General procedure](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl#title-2565-1)
  - [Generate PFX certificate for Windows](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl#title-2565-1)
  - [Generate PFX certificate for Linux](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl#title-2565-6)
- [Change PFX certificate in the existing Identity Service](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl#title-2565-11)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl#see-also)
- [E-learning courses](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl#e-learning-courses)