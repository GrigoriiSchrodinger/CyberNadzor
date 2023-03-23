CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    id_users TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS below_track (
    id INTEGER PRIMARY KEY,
    id_users TEXT NOT NULL UNIQUE,
    bitcoin INTEGER,
    ethereum INTEGER,
    litecoin INTEGER,
    dogecoin INTEGER,
    cardano INTEGER,
    FOREIGN KEY (id_users) REFERENCES users(id_users)
);

CREATE TABLE IF NOT EXISTS higher_track (
    id INTEGER PRIMARY KEY,
    id_users TEXT NOT NULL UNIQUE,
    bitcoin INTEGER,
    ethereum INTEGER,
    litecoin INTEGER,
    dogecoin INTEGER,
    cardano INTEGER,
    FOREIGN KEY (id_users) REFERENCES users(id_users)
);