-- =============================================================================
-- SISTEMA DE RESERVAS CLUB DEPORTIVO ENCUENTRO
-- Script de Inicialización de Base de Datos (init_db.sql)
-- Engine: MySQL 8.0+ / InnoDB / UTF-8 (utf8mb4)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS club_deportivo
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE club_deportivo;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS bloqueos;
DROP TABLE IF EXISTS reservas;
DROP TABLE IF EXISTS socios;
DROP TABLE IF EXISTS canchas;
DROP TABLE IF EXISTS deportes;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE canchas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);

CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    id_cancha INT NOT NULL,
    fecha_hora_inicio VARCHAR(35) NOT NULL,
    fecha_hora_fin VARCHAR(35) NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'finalizada') NOT NULL DEFAULT 'confirmada',
    precio_hora INT NOT NULL,
    precio_total INT NOT NULL,
    FOREIGN KEY (id_socio) REFERENCES socios(id),
    FOREIGN KEY (id_cancha) REFERENCES canchas(id)
);

CREATE TABLE bloqueos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cancha INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    motivo TEXT NOT NULL,
    FOREIGN KEY (id_cancha) REFERENCES canchas(id)
);

INSERT INTO deportes (id, nombre) VALUES
(1, 'Fútbol'),
(2, 'Tenis'),
(3, 'Pádel')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);