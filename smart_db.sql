-- Crear base de datos para el banco
CREATE DATABASE SmartMirrorDB;

-- Usar la recién creada base de datos
USE SmartMirrorDB;

-- Crear la única tabla que contendrá todos los datos de los usuarios del banco
CREATE TABLE `SmartMirror` (
  `id` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `mail` varchar(50),
  `mail_password` varchar(50),
  `news_country` varchar(50),
  `weather_country` varchar(50),
  `weather_city` varchar(50),
  PRIMARY KEY (`id`)
);

-- Insertar registro de usuario
INSERT INTO SmartMirror (id, password, mail, mail_password, news_country, weather_country, weather_city)
VALUES ('9876543210', 'password', 'john@coldmail.com', 'mail_password', 'Mexico', 'Mexico', 'Queretaro');