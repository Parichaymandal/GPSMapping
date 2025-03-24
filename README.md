# GPSMapping

This FastAPI application processes GPS track recordings, maps them to a road network (extracted from OpenStreetMap), and provides endpoints to retrieve the mapped data as GeoJSON.

## Features
- Upload GPS track data in GeoJSON format.
- Store GPS tracks and road network edges in a PostgreSQL/PostGIS database.
- Map GPS track sections to road edges.
- Retrieve mapped GPS track sections as GeoJSON LineString features.
- Dockerized setup for easy deployment.

## Getting Started

### 1. Prerequisites**
Ensure you have the following installed:
- Docker & Docker Compose
- Python 3.9+

### 2. Clone the Repository
```bash
git clone https://github.com/Parichaymandal/GPSMapping
cd GPSMapping
```

### 3. Setup Environment Variables
Create a `.env` file in the root directory with the following content:

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## 4. Run with Docker

To run the app with Docker, follow these steps:

1. Ensure Docker and Docker Compose are installed on your machine. If you haven't installed them yet, you can follow the instructions in the [Docker documentation](https://docs.docker.com/get-docker/).

2. Build and start the containers using the following command:
   ```bash
   docker-compose up --build
   ```


### Access the application:
Once the containers are up and running, you can access the application at the following URLs:
- FastAPI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### To stop the services:
To stop and remove the containers, run the following command:
```bash
docker-compose down
```


