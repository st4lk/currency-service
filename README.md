Currency service
================

### Requirements

- docker (tested on version 2.0.0.3 (31259))
- docker-compose (tested on version 1.23.2, build 1110ad01)
- make (tested on GNU Make 3.81)

### Run

```bash
make run
```

##### Before the first run, create needed tables in database:

```bash
COMMAND=migrate make command
```

Command can be run solely or in another terminal window, in parallel with server running.

### Download currencies

```bash
COMMAND=download_currencies make command
```

This will download currencies `'BTC', 'ETH', 'XRP', 'LTC', 'AIO'` for last 10 days into database.
To specify different currencies, use following syntax:

```bash
COMMAND=download_currencies ARGS='"-c BTC ETH"' make command
```

Command can be run solely or in another terminal window, in parallel with server running.

### Available resources

Open [http://localhost:8080/](http://localhost:8080/) in browser to find available resources.

### Basic Auth

All API resources are protected with Basic Auth. In development, following credentials can be used:

- login: `user`
- password: `password`

### Tests

To run tests, execute the following command:

```bash
make test
```

Note: it is better to stop currently running instance of the project before running the tests.



### Usefull commands

- stop and remove all docker containers:

    ```bash
    make clean
    ```

- access shell in project container:

    ```bash
    make shell
    ```

- access database of the project:

    ```bash
    docker exec -it currency_service_db_sql_1 psql -h 127.0.0.1 -p 5432 -U currency -d currency
    ```

    Note: replace `currency_service_db_sql_1` with the name of your container.
    To find name of currenlty running containers, use

    ```bash
    docker-compose ps
    ```


### TODO:

- setup lint checker
- setup mypy
- setup CI
