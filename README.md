# Mini Zanzibar
Mini-Zanzibar is a simplified version of Google's [Zanzibar](https://zanzibar.academy/) system for global authorization. An access control system has been implemented in Python, along with the creation of a proof of concept client featuring a separate Python server that connects to Mini-Zanzibar and a frontend application. The client represents a software system for managing whiteboards, enabling collaborative work with functionalities for creating, sharing, and deleting boards, in addition to basic drawing and writing options. The TLDraw React library has been used for the whiteboard interface.

## Auth Server
The authorization server is implemented as a Python FastAPI server. For storing ACLs, Google's LevelDB is used, with data stored in the format object#relation@user. It is also possible to configure namespaces, within which access types (e.g., owner, editor) and relationships between users and objects can be defined. ConsulDB with custom versioning is utilized for storing namespaces. An example configuration is provided below:
```
{
    "namespace": "doc",
    "relations": {
        "owner": {},
        "editor": {
            "union": [
                {"this": {}},
                {"computed_userset": {"relation": "owner"}}
            ]
        },
        "viewer": {
            "union": [
                {"this": {}},
                {"computed_userset": {"relation": "editor"}}
            ]
        }
    }
}
```
The functionality of the authorization server is exposed through an API, providing capabilities for creating and modifying ACLs, verifying ACLs, and creating and modifying namespaces.

## Client
The client application aims to create a system for managing whiteboards and collaborative drawing. The server infrastructure is implemented using a FastAPI Python server with PostgreSQL for storage. Access to the whiteboards is regulated using Mini-Zanzibar. The client infrastructure is built with the React framework in TypeScript, utilizing the TLDRAW library for whiteboard functionality.
### Screenshots
![image](https://github.com/user-attachments/assets/de0ab36e-8e2b-487d-ba6e-174be01b25a0)

![image](https://github.com/user-attachments/assets/e2b08332-233b-4761-b094-3f3b82456691)

![image](https://github.com/user-attachments/assets/03edcb9b-6dd8-4fe0-8b7f-b73e5903a458)

## Documentation
- [Security Requirements](https://github.com/jokicjovan/Mini-Zanzibar/blob/main/reports/Security_Requirements.md)
- [Static Code Analysis](https://github.com/jokicjovan/Mini-Zanzibar/blob/main/reports/Static_Code_Analysis.md)
- [Threat Model](https://github.com/jokicjovan/Mini-Zanzibar/blob/main/reports/Threat_Model.md)

## Requirements 
### Mini Zanzibar 
**.env File Variables:**
- `ACL_LEVELDB_PATH`
- `CONSUL_DB_HOST`
- `CONSUL_DB_PORT`

### Backend Client 
**.env File Variables:**
- `DATABASE_URL`
- `SECRET_KEY`
- `MINI_ZANZIBAR_URL`

## Authors

- [Jovan Jokić](https://github.com/jokicjovan)
- [Bojan Mijanović](https://github.com/bmijanovic)
- [Vukašin Bogdanović](https://github.com/vukasinb7)
