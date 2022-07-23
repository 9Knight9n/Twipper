# create databases
CREATE DATABASE IF NOT EXISTS `TwipperDB`;

# create dbadmin user and grant rights
CREATE USER 'dbadmin'@'%' IDENTIFIED BY '123456789';
GRANT ALL ON *.* TO 'dbadmin'@'%';
FLUSH PRIVILEGES;