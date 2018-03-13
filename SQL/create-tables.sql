CREATE DATABASE IF NOT EXISTS `water.db`;
USE `water.db`;
-- clients table
CREATE TABLE IF NOT EXISTS clients (
  `clientID` int(10)  PRIMARY KEY,
  `clientIP` varchar(16) NOT NULL,
  `clientKey` varchar(24) NOT NULL,
  `clientName` varchar(50) NOT NULL,
  `datetime` varchar(50) NOT NULL,
  PRIMARY KEY(clientID)
  );
-- reports table
CREATE TABLE IF NOT EXISTS reports (
  `id` int(10)  PRIMARY KEY,
  `clientID` int(10)  NOT NULL,
  `datetime` varchar(16) NOT NULL,
  `status` int(10) NOT NULL,
  `alarm1` int(1) NOT NULL,
  `alarm2` int(1) NOT NULL,
  PRIMARY KEY(id)
  FOREIGN KEY (clientID) REFERENCES clients (clientID)
);
