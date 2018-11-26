-- Borrar base de datos si es necesario
DROP DATABASE SmartMirrorDB;

-- Crear base de datos para el banco
CREATE DATABASE SmartMirrorDB;

-- Usar la recién creada base de datos
USE SmartMirrorDB;

-- Crear la única tabla que contendrá todos los datos de los usuarios del banco
CREATE TABLE `SmartMirror` (
  `id` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `name` varchar(50),
  `last_name` varchar(50),
  `gender` varchar(1),
  `twitter` varchar(50),
  `twitter_password` varchar(50),
  `mail` varchar(50),
  `mail_password` varchar(50),
  `news_country` varchar(50),
  `weather_country` varchar(50),
  `weather_city` varchar(50),
  PRIMARY KEY (`id`)
);

-- Insertar registro de usuario
INSERT INTO SmartMirror (id, password, name, last_name, gender, mail, mail_password, news_country, weather_country, weather_city)
VALUES ('9876543210', 'password', 'John', 'Doe', 'M', 'john@coldmail.com', 'mail_password', 'Mexico', 'Mexico', 'Queretaro');