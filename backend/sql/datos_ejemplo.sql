-- ============================================================
-- Datos de ejemplo: dueño, mascota, fotos y eventos médicos
-- Ejecutar después de esquema.sql
-- ============================================================

USE ficha_mascotas;

-- ------------------------------------------------------------
-- Dueño de ejemplo
-- ------------------------------------------------------------
INSERT INTO duenos (
    id, nombre, foto,
    whatsapp, whatsapp_url,
    telegram, telegram_url,
    facebook, facebook_url,
    instagram, instagram_url,
    tiktok, tiktok_url,
    email, direccion
) VALUES (
    1,
    'Pablo Herrera',
    'public/dueno.svg',
    '+54 9 11 0000-0000',
    'https://wa.me/5491100000000',
    '@usuario',
    'https://t.me/usuario',
    '/usuario',
    'https://www.facebook.com/usuario',
    '@usuario',
    'https://www.instagram.com/usuario',
    '@usuario',
    'https://www.tiktok.com/@usuario',
    'correo@ejemplo.com',
    'Calle 123, Ciudad'
) AS nuevo
ON DUPLICATE KEY UPDATE
    nombre = nuevo.nombre,
    foto = nuevo.foto,
    whatsapp = nuevo.whatsapp,
    whatsapp_url = nuevo.whatsapp_url,
    telegram = nuevo.telegram,
    telegram_url = nuevo.telegram_url,
    facebook = nuevo.facebook,
    facebook_url = nuevo.facebook_url,
    instagram = nuevo.instagram,
    instagram_url = nuevo.instagram_url,
    tiktok = nuevo.tiktok,
    tiktok_url = nuevo.tiktok_url,
    email = nuevo.email,
    direccion = nuevo.direccion;

-- ------------------------------------------------------------
-- Mascota de ejemplo
-- ------------------------------------------------------------
INSERT INTO mascotas (
    id, dueno_id, nombre, especie, raza, edad, foto,
    descripcion, personalidad,
    peso_kg, altura_cm,
    vacunas, alergias, enfermedades, veterinario
) VALUES (
    1,
    1,
    'Duke',
    'Perro',
    'Ovejero Alemán',
    '4 años',
    'public/fotoprincipal.webp',
    'Soy un perro muy protector, inteligente y cariñoso.',
    'Soy muy enérgico, atento y me llevo bien con todos.',
    30.00,
    56.00,
    'Al día',
    'Ninguna conocida',
    'Ninguna',
    'Dr. Martínez - Clínica Animal Feliz'
) AS nuevo
ON DUPLICATE KEY UPDATE
    dueno_id = nuevo.dueno_id,
    nombre = nuevo.nombre,
    especie = nuevo.especie,
    raza = nuevo.raza,
    edad = nuevo.edad,
    foto = nuevo.foto,
    descripcion = nuevo.descripcion,
    personalidad = nuevo.personalidad,
    peso_kg = nuevo.peso_kg,
    altura_cm = nuevo.altura_cm,
    vacunas = nuevo.vacunas,
    alergias = nuevo.alergias,
    enfermedades = nuevo.enfermedades,
    veterinario = nuevo.veterinario;

-- ------------------------------------------------------------
-- Galería de Duke
-- ------------------------------------------------------------
INSERT INTO mascota_fotos (id, mascota_id, ruta, descripcion, orden) VALUES
    (1, 1, 'public/fotoprincipal.webp', 'Duke descansando', 0),
    (2, 1, 'public/album01.jpg', 'Duke 1', 1),
    (3, 1, 'public/album02.jpg', 'Duke 2', 2),
    (4, 1, 'public/album03.jpg', 'Duke 3', 3),
    (5, 1, 'public/album04.jpeg', 'Duke 4', 4),
    (6, 1, 'public/album05.jpg', 'Duke 5', 5),
    (7, 1, 'public/album06.jpeg', 'Duke 6', 6),
    (8, 1, 'public/album07.jpg', 'Duke 7', 7),
    (9, 1, 'public/album08.jpg', 'Duke 8', 8),
    (10, 1, 'public/album09.jpg', 'Duke 9', 9),
    (11, 1, 'public/album10.jpeg', 'Duke 10', 10),
    (12, 1, 'public/album11.jpeg', 'Duke 11', 11) AS nuevo
ON DUPLICATE KEY UPDATE
    mascota_id = nuevo.mascota_id,
    ruta = nuevo.ruta,
    descripcion = nuevo.descripcion,
    orden = nuevo.orden;

-- ------------------------------------------------------------
-- Eventos médicos de Duke
-- ------------------------------------------------------------
INSERT INTO mascota_eventos_medicos (id, mascota_id, tipo, descripcion, fecha) VALUES
    (1, 1, 'Fractura',
     'Fractura de la pata delantera izquierda, tratada con inmovilización y rehabilitación.',
     '2022-02-01'),
    (2, 1, 'Infección de oído',
     'Infección de oído leve tratada con antibióticos.',
     '2022-10-01') AS nuevo
ON DUPLICATE KEY UPDATE
    mascota_id = nuevo.mascota_id,
    tipo = nuevo.tipo,
    descripcion = nuevo.descripcion,
    fecha = nuevo.fecha;
