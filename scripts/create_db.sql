CREATE DATABASE codesearch;

CREATE USER 'codesearch'@'localhost' IDENTIFIED BY 'codesearch';
GRANT ALL PRIVILEGES ON codesearch.* TO 'codesearch'@'localhost' IDENTIFIED BY 'codesearch';
FLUSH PRIVILEGES;

USE codesearch;

CREATE TABLE documents (id INTEGER, path VARCHAR(255), project VARCHAR(255), text LONGBLOB);
