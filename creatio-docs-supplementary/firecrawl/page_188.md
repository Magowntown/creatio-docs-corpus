<!-- Source: page_188 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/freedom-ui/customize-page/references/folder-management-menu-mobile#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Level: beginner

Use the **Folder management menu** component to open the page folder tree.

View the example of a configuration object that opens the page folder tree below.

Example of a configuration object that opens the page folder tree

```js
{
    "type": "crt.FolderTreeActions",
    "caption": "Folders",
    "name": "MyFolderTree",
    "sourceSchemaName": "ContactFolder",
    "folderTreeVisibleChanged": {
        "request": "crt.OpenModalFolderTreeRequest",
        "params": {
            "folderTreeConfig": {
                "caption": "Select folder",
                "sourceSchemaName": "ContactFolder",
                "rootSchemaName": "Contact"
            }
        }
    }
}
```

* * *

```js
string type
```

Component type. `crt.FolderTreeActions` for the **Folder management menu** component.

* * *

```js
string caption
```

Component caption.

* * *

```js
string name
```

Component name.

* * *

```js
string sourceSchemaName
```

Entity schema that stores a list of folders.

* * *

```js
string activeFolderName
```

Out-of-the-box selected folder. Required.

* * *

```js
object folderTreeVisibleChanged
```

The `crt.OpenModalFolderTreeRequest` base request that opens a list of folders.