CREATE TABLE
IF NOT EXISTS clients (
 clientID integer PRIMARY KEY,
 clientIP text NOT NULL,
 clientKey text NOT NULL,
 clientName text NOT NULL,
 date text NOT NULL
);

-- tasks table
CREATE TABLE
IF NOT EXISTS reports (
 id integer PRIMARY KEY,
 clientID integer FOREIGN KEY,
 datetime text NOT NULL,
 status text NOT NULL,
 alarm1 integer NOT NULL,
 alarm2 integer NOT NULL,
 message text,
 FOREIGN KEY (clientID) REFERENCES clients (clientID)
);