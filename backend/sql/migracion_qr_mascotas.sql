USE ficha_mascotas;

CREATE TABLE IF NOT EXISTS mascota_qr (
    mascota_id INT UNSIGNED NOT NULL,
    ruta_ficha VARCHAR(255) NOT NULL,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (mascota_id),
    CONSTRAINT fk_mascota_qr_mascota
        FOREIGN KEY (mascota_id) REFERENCES mascotas (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
