# create databases
CREATE DATABASE IF NOT EXISTS `TwipperDB`;

# create dbadmin user and grant rights
CREATE USER 'dbadmin'@'%' IDENTIFIED BY 'rS9ytkgUxFo9z#';
GRANT ALL ON *.* TO 'dbadmin'@'%';
FLUSH PRIVILEGES;