CREATE DATABASE IF NOT EXISTS weather_zp_app;

USE weather_zp_app;

CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    email VARCHAR(320) NOT NULL UNIQUE,
    gender BLOB, 
    birsday DATE,
    CHECK (
		(first_name != '') AND
        (last_name != '') AND
        (email != ''))
	);

CREATE TABLE IF NOT EXISTS feedback (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(320) NOT NULL,
    message TEXT NOT NULL,
    CHECK (
		(name != '') AND
        (email != '') AND
        (message != ''))
	);