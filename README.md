# Installation
1. Create a venv
2. Install Requirements
3. Set env vars in a .env file
```bash
MONGO_PASSWORD=example
MONGO_URL=mongodb+srv://username:${MONGO_PASSWORD}@examplemongo.com
MONGO_DATABASE_NAME=database
```


## Set the required environment variables:

- MONGO_PASSWORD: [description]
- MONGO_URL: [description]
- MONGO_DATABASE_NAME: [description]
- PREAUTHMAIL: [description]
- ADMINUSERS: [description]

## Build Docker Image

``` bash
docker build -t streamlit-app .
```

## Run the Docker container

```bash
docker run -d -p 8501:8501 --name streamlit-container streamlit-app
```