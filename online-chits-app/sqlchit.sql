DROP TABLE IF EXISTS CHIT;

CREATE TABLE CHIT (
    name text not NULL,
    owner text not NULL,
    fundsize integer not NULL,
    nopeople integer not NULL,
    fdate text NOT NULL,
    tdate text NOT NULL,
    pdate text NOT NULL
)