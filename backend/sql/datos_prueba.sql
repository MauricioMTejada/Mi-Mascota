-- ============================================================
-- Datos de prueba: 4 dueños ficticios y 6 mascotas ficticias
-- Ejecutar después de esquema.sql y datos_ejemplo.sql
-- ============================================================

USE ficha_mascotas;

-- ------------------------------------------------------------
-- Dueños ficticios (IDs 2 a 5)
-- ------------------------------------------------------------
INSERT INTO duenos (
    id, nombre, foto,
    whatsapp, whatsapp_url,
    telegram, telegram_url,
    facebook, facebook_url,
    instagram, instagram_url,
    tiktok, tiktok_url,
    email, direccion
) VALUES
    (
        2,
        'Lucía Fernández',
        'public/dueno.svg',
        '+54 9 11 5555-1002',
        'https://wa.me/5491155551002',
        '@luciafer',
        'https://t.me/luciafer',
        '/lucia.fernandez.demo',
        'https://www.facebook.com/lucia.fernandez.demo',
        '@lucia.fer.demo',
        'https://www.instagram.com/lucia.fer.demo',
        '@luciaferdemo',
        'https://www.tiktok.com/@luciaferdemo',
        'lucia.fernandez@example.com',
        'Av. Rivadavia 2450, CABA'
    ),
    (
        3,
        'Martín Rodríguez',
        'public/dueno.svg',
        '+54 9 351 555-2003',
        'https://wa.me/5493515552003',
        '@martinrod',
        'https://t.me/martinrod',
        '/martin.rodriguez.demo',
        'https://www.facebook.com/martin.rodriguez.demo',
        '@martin.rod.demo',
        'https://www.instagram.com/martin.rod.demo',
        '@martinroddemo',
        'https://www.tiktok.com/@martinroddemo',
        'martin.rodriguez@example.com',
        'Av. Colón 850, Córdoba'
    ),
    (
        4,
        'Sofía Benítez',
        'public/dueno.svg',
        '+54 9 341 555-3004',
        'https://wa.me/5493415553004',
        '@sofiaben',
        'https://t.me/sofiaben',
        '/sofia.benitez.demo',
        'https://www.facebook.com/sofia.benitez.demo',
        '@sofia.ben.demo',
        'https://www.instagram.com/sofia.ben.demo',
        '@sofiabendemo',
        'https://www.tiktok.com/@sofiabendemo',
        'sofia.benitez@example.com',
        'Bv. Oroño 1200, Rosario'
    ),
    (
        5,
        'Diego Ramírez',
        'public/dueno.svg',
        '+54 9 261 555-4005',
        'https://wa.me/5492615554005',
        '@diegoram',
        'https://t.me/diegoram',
        '/diego.ramirez.demo',
        'https://www.facebook.com/diego.ramirez.demo',
        '@diego.ram.demo',
        'https://www.instagram.com/diego.ram.demo',
        '@diegoramdemo',
        'https://www.tiktok.com/@diegoramdemo',
        'diego.ramirez@example.com',
        'Av. San Martín 1500, Mendoza'
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
-- Mascotas ficticias (IDs 2 a 7)
-- ------------------------------------------------------------
INSERT INTO mascotas (
    id, dueno_id, nombre, especie, raza, edad, foto,
    descripcion, personalidad,
    peso_kg, altura_cm,
    vacunas, alergias, enfermedades, veterinario
) VALUES
    (
        2, 2, 'Luna', 'Gata', 'Siamesa', '2 años',
        'public/mascota-generica.svg',
        'Soy una gata tranquila y muy curiosa.',
        'Me encanta dormir al sol y observar todo desde lo alto.',
        4.20, 25.00,
        'Al día', 'Ninguna conocida', 'Ninguna',
        'Dra. Gómez - Clínica Veterinaria Palermo'
    ),
    (
        3, 2, 'Rocky', 'Perro', 'Bulldog Francés', '3 años',
        'public/mascota-generica.svg',
        'Soy un perro juguetón y muy compañero.',
        'Disfruto de los paseos cortos y de jugar con pelotas.',
        12.50, 32.00,
        'Al día', 'Alergia al pollo', 'Ninguna',
        'Dr. Pérez - Veterinaria del Sur'
    ),
    (
        4, 3, 'Milo', 'Perro', 'Golden Retriever', '5 años',
        'public/mascota-generica.svg',
        'Soy un perro sociable, obediente y muy cariñoso.',
        'Me llevo bien con todos y me encanta el agua.',
        29.00, 58.00,
        'Al día', 'Ninguna conocida', 'Displasia leve de cadera',
        'Dr. Molina - Clínica Animal Córdoba'
    ),
    (
        5, 4, 'Nina', 'Gata', 'Persa', '1 año',
        'public/mascota-generica.svg',
        'Soy una gata tranquila y muy mimosa.',
        'Prefiero los lugares cálidos y las siestas largas.',
        3.80, 22.00,
        'Al día', 'Ninguna conocida', 'Ninguna',
        'Dra. Rossi - Veterinaria Central Rosario'
    ),
    (
        6, 4, 'Simba', 'Perro', 'Mestizo', '6 años',
        'public/mascota-generica.svg',
        'Soy un perro noble y protector.',
        'Me gusta cuidar la casa y acompañar a mi familia.',
        22.00, 48.00,
        'Al día', 'Ninguna conocida', 'Artrosis incipiente',
        'Dra. Rossi - Veterinaria Central Rosario'
    ),
    (
        7, 5, 'Coco', 'Conejo', 'Enano', '2 años',
        'public/mascota-generica.svg',
        'Soy un conejo curioso y bastante tranquilo.',
        'Disfruto explorar y comer verduras frescas.',
        1.80, 20.00,
        'No requiere', 'Ninguna conocida', 'Ninguna',
        'Dr. Sosa - Clínica de Animales Exóticos'
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
-- Una foto genérica para cada mascota ficticia
-- ------------------------------------------------------------
INSERT INTO mascota_fotos (id, mascota_id, ruta, descripcion, orden) VALUES
    (13, 2, 'public/mascota-generica.svg', 'Luna - foto de ejemplo', 0),
    (14, 3, 'public/mascota-generica.svg', 'Rocky - foto de ejemplo', 0),
    (15, 4, 'public/mascota-generica.svg', 'Milo - foto de ejemplo', 0),
    (16, 5, 'public/mascota-generica.svg', 'Nina - foto de ejemplo', 0),
    (17, 6, 'public/mascota-generica.svg', 'Simba - foto de ejemplo', 0),
    (18, 7, 'public/mascota-generica.svg', 'Coco - foto de ejemplo', 0) AS nuevo
ON DUPLICATE KEY UPDATE
    mascota_id = nuevo.mascota_id,
    ruta = nuevo.ruta,
    descripcion = nuevo.descripcion,
    orden = nuevo.orden;

-- ------------------------------------------------------------
-- Algunos eventos médicos de prueba
-- ------------------------------------------------------------
INSERT INTO mascota_eventos_medicos (id, mascota_id, tipo, descripcion, fecha) VALUES
    (
        3, 4, 'Control de cadera',
        'Diagnóstico de displasia leve. Se recomienda control anual y ejercicios de bajo impacto.',
        '2025-06-15'
    ),
    (
        4, 6, 'Artrosis',
        'Artrosis incipiente detectada en control geriátrico. Se indicó suplementación.',
        '2026-01-20'
    ) AS nuevo
ON DUPLICATE KEY UPDATE
    mascota_id = nuevo.mascota_id,
    tipo = nuevo.tipo,
    descripcion = nuevo.descripcion,
    fecha = nuevo.fecha;
