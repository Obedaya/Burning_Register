# Installation
1. Create a venv
2. Install Requirements
3. Set env vars in a .env file
```bash
MONGO_PASSWORD=example
MONGO_URL=mongodb+srv://username:${MONGO_PASSWORD}@examplemongo.com
PREAUTHMAIL=test@example.com,test2@example.com
ADMINUSERS=testuser,testuser2
```