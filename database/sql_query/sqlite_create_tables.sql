CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    id_users TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS below_track (
    id INTEGER PRIMARY KEY,
    bitcoin INTEGER,
    ethereum INTEGER,
    litecoin INTEGER,
    dogecoin INTEGER,
    cardano INTEGER,
    FOREIGN KEY (id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS higher_track (
    id INTEGER PRIMARY KEY,
    bitcoin INTEGER,
    ethereum INTEGER,
    litecoin INTEGER,
    dogecoin INTEGER,
    cardano INTEGER,
    FOREIGN KEY (id) REFERENCES users(id)
);