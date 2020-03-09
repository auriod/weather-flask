CREATE DATABASE IF NOT EXISTS weather_zp_app;

USE weather_zp_app;

-- таблица с данными пользователей
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

-- таблица для сообщений
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

-- таблица связи пользователь-сообщение
CREATE TABLE IF NOT EXISTS user_feedback (
	user_id INTEGER NOT NULL,
    feedback_id INTEGER NOT NULL,
    FOREIGN KEY (user_id)
		REFERENCES users(id)
        ON DELETE CASCADE,
	FOREIGN KEY (feedback_id)
		REFERENCES feedback(id)
        ON DELETE CASCADE
	);

