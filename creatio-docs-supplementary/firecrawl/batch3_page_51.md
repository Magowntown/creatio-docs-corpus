<!-- Source:  -->

[Skip to main content](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/setup-and-administration/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments)** (8.3).

Version: 8.2All Creatio products

On this page

Version control is required for deploying a development environment where several developers can commit, monitor, and merge the changes made to the Creatio configuration. The purpose of the version control system in Creatio is:

- transferring of changes between configurations
- storing multiple versions of configuration schemas
- rolling back changes to return to one of the previous versions.

Creatio supports integration with the Subversion control system (SVN) of version 1.14 and later. For more details on using SVN see [Subversion control system documentation](http://svnbook.red-bean.com/).

note

Creatio native development tools work only with the Subversion version control system. However, you can disable version control integration and use any version control system, including Git, when developing in the "File system development mode". Learn more about working with Git in Creatio in our [SDK guide](https://academy.creatio.com/documents/technic-sdk/7-16/working-git).

An SVN repository should be the only point of contact for different development environments. Otherwise, the development environment of each developer must be insulated and run on an independent application server connected to a database not used by other Creatio application instances.

More information on setting up a development environment is available [in the Development Guide](https://academy.creatio.com/documents/technic-sdk/7-16/development-environment).

The general procedure for setting up and connecting SVN is as follows:

- [Deploy SVN and create a Creatio repository](https://academy.creatio.com/#XREF_23418_Deploy_SVN_and)
- [Connect the repository to Creatio](https://academy.creatio.com/#XREF_43443_Connect_the)

## Deploy SVN and create a Creatio repository [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments\#title-273-1 "Direct link to Deploy SVN and create a Creatio repository")

To deploy Subversion for your Creatio application:

### 1\. Install SVN server [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments\#title-273-2 "Direct link to 1. Install SVN server")

You can install SVN on the application server, DBMS server or on a separate dedicated server.

To install the SVN server on a Windows operating system, use one of the publicly available SVN installers:

- [VisualSVN](https://www.visualsvn.com/server/)
- [CollabNet](http://www.collab.net/products/subversion)

Installation instructions for other operating systems, including Debian, are available with [Apache Subversion](http://subversion.apache.org/packages.html).

The SVN server can function independently or use an Apache web-server as a frontend (both the VisualSVN and CollabNet utilities can install it as a component).

If the SVN server is running independently, repositories are accessed through the **SVN** protocol. If a web server is used as a frontend, repositories are accessed through the **HTTP** and **HTTPS** protocols.

We recommend installing a web-server frontend and using the webserver protocols ( **HTTP** and **HTTPS**) for integration with Creatio.

### 2\. Create a user on the SVN server [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments\#title-273-3 "Direct link to 2. Create a user on the SVN server")

To access the SVN server, add at least one SVN user. We recommend creating a separate user for each developer.

You can create an SVN server user with the standard tools supplied with the SVN server installation package, for example, VisualSVN ( [Fig. 1](https://academy.creatio.com/#XREF_11187_Fig_5_Creating_a)).

Working with the Creatio repository requires password-based authentication.

Fig. 1 Creating a new user in the SVN server (VisualSVN utility)

![Fig. 1 Creating a new user in the SVN server (VisualSVN utility)](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/version_control_for_dev_env/scr_svn_getting_started_visual_svn.png)

### 3\. Create a repository on the SVN server [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments\#title-273-4 "Direct link to 3. Create a repository on the SVN server")

Create an SVN repository using the standard tools supplied with the SVN server installation package (i.e., VisualSVN and CollabNet).

note

Creatio supports the simultaneous operation of several repositories that can be located on different SVN servers.

### 4\. Install SVN client (optional) [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments\#title-273-5 "Direct link to 4. Install SVN client (optional)")

You can optionally install an SVN client in the developer workplace, for example, [TortoiseSVN](http://tortoisesvn.net/).

note

We recommend using TortoiseSVN client version 1.14 and up.

Installing an SVN client is not required since it does not affect the Creatio operation. Using an SVN client is convenient for viewing the local working copy, history, revert operations, review, etc.

## Connect the repository to Creatio [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments\#title-273-6 "Direct link to Connect the repository to Creatio")

To connect an SVN repository to Creatio:

1. Copy the URL of your repository. For example, in VisualSVN, right-click the repository → **Copy URL to clipboard** ( [Fig. 1](https://academy.creatio.com/#XREF_50820_Fig_6_Copy_the_URL)).
Fig. 1 Copy the URL of the repository

![Fig. 1 Copy the URL of the repository](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/version_control_for_dev_env/scr_setup_svn_copy_url.png)

2. Click ![btn_system_designer.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/version_control_for_dev_env/btn_system_designer.png) in the main Creatio application. The System Designer will open.

3. Click **Advanced settings** in the **Admin area** to open the **Configuration** section.

4. Click **Open list of repositories** on the **Actions** tab ( [Fig. 2](https://academy.creatio.com/#XREF_94530_Fig_7_Open_the)).
Fig. 2 Opening the SVN repository list

![Fig. 2 Opening the SVN repository list](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/version_control_for_dev_env/scr_setup_svn_open_list_of_repositories.png)

5. Click **Add** on the list toolbar ( [Fig. 3](https://academy.creatio.com/#XREF_37901_Fig_6_Window_with)). A page for the new repository will open.
Fig. 3 Adding a new repository to the list of version control system repositories

![Fig. 3 Adding a new repository to the list of version control system repositories](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/version_control_for_dev_env/scr_setup_additional_using_several_svn_storages.png)

6. In the new repository page, specify the repository data ( [Fig. 4](https://academy.creatio.com/#XREF_21746_Fig_7_New)).
Fig. 4 Entering the repository data in the repository page

![Fig. 4 Entering the repository data in the repository page](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/version_control_for_dev_env/scr_svn_adding_new_repository.png)


**Name** – repository name.

**Storage address** – the network address of an existing SVN repository. Insert the URL that you copied on step 1 of this instruction.

The HTTP protocol (standard network protocol), HTTPS protocol (standard network protocol secured with SSL encryption), and SVN protocol (own network protocol of the Subversion system) are all supported in repository addressing.

**Active** – select this checkbox to enable using the repository in the system operation. Each new repository is marked as active by default.



note





You can work with active repositories only. Moreover, all repositories, from which the packages are updated, must be active. These include the repository from which the initial package is updated and the repositories from which all packages-dependencies of the initial package are updated.

7. Click the repository in the repository list → **Authenticate** ( [Fig. 5](https://academy.creatio.com/#XREF_57800_Fig_10)).
Fig. 5 Authenticating a repository

![Fig. 5 Authenticating a repository](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/version_control_for_dev_env/scr_setup_additional_svn_authenticate.png)

8. Authenticate to your SVN repository using one of the users you have created on your SVN server ( [Fig. 6](https://academy.creatio.com/#XREF_81513_Fig_11_Providing)).
Fig. 6 Providing SVN credentials

![Fig. 6 Providing SVN credentials](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/on_site_deployment/BPMonlineHelp/version_control_for_dev_env/scr_svn_setup_credentials.png)


As a result, your SVN repository will be connected to Creatio. Use the new repository to create user-made packages and install the created packages in the workspace.

Learn more about [working with packages using SVN](https://academy.creatio.com/documents/technic-sdk/7-16/version-control-system-built-ide), [transferring changes using SVN](https://academy.creatio.com/documents/technic-sdk/7-16/transferring-changes-using-svn), and [working with SVN](https://academy.creatio.com/documents/technic-sdk/7-16/subversion) in general in our SDK guide.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments\#see-also "Direct link to See also")

[Working with packages using SVN](https://academy.creatio.com/documents/technic-sdk/7-16/version-control-system-built-ide)

[Transferring changes using SVN](https://academy.creatio.com/documents/technic-sdk/7-16/transferring-changes-using-svn)

[Working with SVN](https://academy.creatio.com/documents/technic-sdk/7-16/subversion)

- [Deploy SVN and create a Creatio repository](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments#title-273-1)
  - [1\. Install SVN server](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments#title-273-2)
  - [2\. Create a user on the SVN server](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments#title-273-3)
  - [3\. Create a repository on the SVN server](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments#title-273-4)
  - [4\. Install SVN client (optional)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments#title-273-5)
- [Connect the repository to Creatio](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments#title-273-6)
- [See also](https://academy.creatio.com/docs/8.x/setup-and-administration/8.2/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments#see-also)