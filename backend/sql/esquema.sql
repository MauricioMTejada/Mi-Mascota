-- ============================================================
-- Base de datos: ficha_mascotas
-- Tablas: dueños, mascotas, fotos y eventos médicos
-- ============================================================

CREATE DATABASE IF NOT EXISTS ficha_mascotas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ficha_mascotas;

-- ------------------------------------------------------------
-- Dueños
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS duenos (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(120) NOT NULL,
    foto VARCHAR(255) DEFAULT NULL,
    whatsapp VARCHAR(40) DEFAULT NULL,
    whatsapp_url VARCHAR(255) DEFAULT NULL,
    telegram VARCHAR(100) DEFAULT NULL,
    telegram_url VARCHAR(255) DEFAULT NULL,
    facebook VARCHAR(100) DEFAULT NULL,
    facebook_url VARCHAR(255) DEFAULT NULL,
    instagram VARCHAR(100) DEFAULT NULL,
    instagram_url VARCHAR(255) DEFAULT NULL,
    tiktok VARCHAR(100) DEFAULT NULL,
    tiktok_url VARCHAR(255) DEFAULT NULL,
    email VARCHAR(150) DEFAULT NULL,
    direccion VARCHAR(255) DEFAULT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Mascotas
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mascotas (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    dueno_id INT UNSIGNED NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(60) NOT NULL DEFAULT 'Perro',
    raza VARCHAR(100) DEFAULT NULL,
    edad VARCHAR(50) DEFAULT NULL,
    fecha_nacimiento DATE DEFAULT NULL,
    foto VARCHAR(255) DEFAULT NULL,
    descripcion TEXT,
    personalidad TEXT,
    peso_kg DECIMAL(5,2) DEFAULT NULL,
    altura_cm DECIMAL(5,2) DEFAULT NULL,
    vacunas VARCHAR(255) DEFAULT NULL,
    alergias VARCHAR(255) DEFAULT NULL,
    enfermedades VARCHAR(255) DEFAULT NULL,
    veterinario VARCHAR(150) DEFAULT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_mascotas_dueno (dueno_id),
    CONSTRAINT fk_mascotas_dueno
        FOREIGN KEY (dueno_id) REFERENCES duenos (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Galería de fotos de cada mascota
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mascota_fotos (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    mascota_id INT UNSIGNED NOT NULL,
    ruta VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) DEFAULT NULL,
    orden INT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    KEY idx_fotos_mascota (mascota_id),
    CONSTRAINT fk_fotos_mascota
        FOREIGN KEY (mascota_id) REFERENCES mascotas (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Historial médico de cada mascota
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mascota_eventos_medicos (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    mascota_id INT UNSIGNED NOT NULL,
    tipo VARCHAR(80) NOT NULL,
    descripcion TEXT,
    fecha DATE DEFAULT NULL,
    PRIMARY KEY (id),
    KEY idx_eventos_mascota (mascota_id),
    CONSTRAINT fk_eventos_mascota
        FOREIGN KEY (mascota_id) REFERENCES mascotas (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Vista de apoyo: relación dueño -> mascotas
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vista_duenos_mascotas AS
SELECT
    d.id AS dueno_id,
    d.nombre AS dueno,
    d.email,
    d.direccion,
    m.id AS mascota_id,
    m.nombre AS mascota,
    m.especie,
    m.raza,
    m.edad
FROM duenos d
LEFT JOIN mascotas m ON m.dueno_id = d.id;
