# Project Database Setup

This setup uses a PostgreSQL container managed with Docker Compose. Configuration is loaded from a `.env` file, and the database is initialized with an SQL script. Data is stored persistently, so it remains available across container restarts.

## Prerequisites

-   Docker and Docker Compose installed on your system.
-   A `.env` file in the project root with the required environment variables.

## Getting Started

#### 1. Create the `.env` file

In the project root, create a `.env` file with the following content:

```plaintext
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
PGDATA_PATH=./pgdata
```

-   `POSTGRES_USER`: PostgreSQL username.
-   `POSTGRES_PASSWORD`: Password for the user.
-   `POSTGRES_DB`: Name of the database to be created.
-   `PGDATA_PATH`: Path where data will be stored persistently.

#### 2. Ensure the init.sql file is Ready

The init.sql file should be in the project root. This script will run automatically the first time the container is started to initialize the database schema and data.

> TODO: Do initalization with ORM instead of init.sql

#### 3. Run Docker Compose

In the project root, run the following command to start the PostgreSQL container:

```shell
docker-compose up -d
```

This command will:

1. Start the PostgreSQL container.
2. Use the `.env` file for configuration.
3. Initialize the database with `init.sql`.
4. Save data persistently in the path specified by `PGDATA_PATH`.

#### 4. Stopping the Container

To stop the container, run:

```shell
docker-compose down
```

Data will remain available because it’s saved in the pgdata directory.

#### 5. If you add new table to init.sql

First run

```shell
docker-compose down -v
```

Delete pgdata folder

```shell
# for unix
rm -rf ./pgdata

# for windows cmd
rmdir /s /q .\pgdata

# for windows powershell
Remove-Item -Recurse -Force .\pgdata
```

and then

```shell
docker-compose up --build
```

#### 6. Accessing the Database

You can access the database with any PostgreSQL client using the credentials in the `.env` file on port `5432 (default postgresql port)`.

## Notes

-   Any changes to `.env` require restarting the container.
-   Persistent data will remain in the `pgdata` directory even if the container is removed.
