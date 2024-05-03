DROP TABLE IF EXISTS posts;

CREATE TABLE USER (
    name text not NULL,
    uname text not NULL,
    email text not NULL,
    password text not NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    phone_no integer(10)
)