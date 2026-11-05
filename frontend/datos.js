// Carga una mascota desde la API y completa la ficha.
// Uso: /?id=3 (si no se indica un ID, muestra la mascota 1).
// Si la página se abre como archivo (file://), conserva los datos del HTML.
(async function () {
    const params = new URLSearchParams(window.location.search);
    const idTexto = params.get("id") || params.get("mascota");
    const mascotaId = idTexto && /^\d+$/.test(idTexto) ? Number(idTexto) : 1;

    try {
        const respuestaMascota = await fetch(`api/mascotas/${mascotaId}`, {
            cache: "no-store",
        });

        if (!respuestaMascota.ok) {
            mostrarError(`No existe una mascota con ID ${mascotaId}.`);
            return;
        }

        const mascota = await respuestaMascota.json();
        const dueno = mascota.dueno || {};

        llenarDueno(dueno);
        llenarMascota(mascota, dueno);
    } catch (error) {
        // Sin servidor disponible: se conservan los datos estáticos del HTML.
    }

    function mostrarError(mensaje) {
        const caja = document.getElementById("mensaje-error");
        if (!caja) {
            return;
        }
        caja.textContent = mensaje;
        caja.hidden = false;
    }

    function llenarDueno(dueno) {
        if (!dueno || !dueno.contactos) {
            return;
        }

        document.querySelectorAll('[data-campo="nombre"]').forEach((elemento) => {
            elemento.textContent = dueno.nombre || "";
        });

        const foto = document.getElementById("foto-dueno");
        if (foto && dueno.foto) {
            foto.src = dueno.foto;
            foto.alt = `Foto de ${dueno.nombre}`;
        }

        Object.entries(dueno.contactos).forEach(([clave, contacto]) => {
            document.querySelectorAll(`[data-campo="${clave}"]`).forEach((elemento) => {
                if (contacto.texto) {
                    elemento.textContent = contacto.texto;
                }
                if (elemento.tagName === "A" && contacto.url) {
                    elemento.href = contacto.url;
                }
            });
        });

        const qr = document.getElementById("qr-imagen");
        if (qr && dueno.id) {
            qr.src = `api/qr?dueno_id=${dueno.id}`;
        }
    }

    function llenarMascota(mascota, dueno) {
        const nombre = mascota.nombre || "Mi mascota";
        const fotoPrincipal = mascota.foto || "public/mascota-generica.svg";

        document.title = `Ficha de ${nombre}`;
        setTexto("titulo-pagina", `Ficha de ${nombre}`);
        setTexto("nombre-mascota", `¡Hola! Soy ${nombre}`);
        setTexto("edad-mascota", mascota.edad || "—");
        setTexto("raza-mascota", mascota.raza || "—");
        setTexto("especie-mascota", mascota.especie || "—");
        setTexto("descripcion-mascota", mascota.descripcion || "");
        setTexto("personalidad-mascota", mascota.personalidad || "");
        setTexto("tabs-titulo", `📋 ¿Quieres saber más sobre ${nombre}?`);

        document.querySelectorAll("[data-nombre-mascota]").forEach((elemento) => {
            elemento.textContent = nombre;
        });

        const foto = document.getElementById("foto-mascota");
        if (foto) {
            foto.src = fotoPrincipal;
            foto.alt = `${nombre} (${mascota.especie || "mascota"})`;
        }

        const fotos = Array.isArray(mascota.fotos) ? mascota.fotos : [];
        const fotoSecundaria = fotos[1]?.ruta || fotos[0]?.ruta || fotoPrincipal;

        const fotoPersonalidad = document.getElementById("foto-personalidad");
        if (fotoPersonalidad) {
            fotoPersonalidad.src = fotoSecundaria;
            fotoPersonalidad.alt = `${nombre} jugando`;
        }

        const enlacePersonalidad = document.getElementById("enlace-foto-personalidad");
        if (enlacePersonalidad) {
            enlacePersonalidad.href = fotoSecundaria;
        }

        const especie = mascota.especie ? mascota.especie.toLowerCase() : "mascota";
        const raza = mascota.raza ? ` de raza ${mascota.raza}` : "";
        setTexto(
            "historia-mascota",
            `${nombre} es un ${especie}${raza}. ${mascota.descripcion || ""}`.trim(),
        );

        const fotoHistoria = document.getElementById("foto-historia");
        if (fotoHistoria) {
            fotoHistoria.src = fotoPrincipal;
            fotoHistoria.alt = nombre;
        }
        setTexto("leyenda-historia", `${nombre} en su foto principal.`);

        llenarGaleria(fotos, fotoPrincipal, nombre);
        llenarTablaMedica(mascota);
        llenarMapa(dueno);
    }

    function llenarGaleria(fotos, fotoPrincipal, nombre) {
        const galeria = document.getElementById("galeria-mascota");
        if (!galeria) {
            return;
        }

        const lista = fotos.length
            ? fotos
            : [{ ruta: fotoPrincipal, descripcion: nombre }];

        galeria.innerHTML = "";
        lista.forEach((foto) => {
            const img = document.createElement("img");
            img.src = foto.ruta;
            img.alt = foto.descripcion || nombre;
            img.loading = "lazy";
            galeria.appendChild(img);
        });
    }

    function llenarTablaMedica(mascota) {
        const tabla = document.getElementById("tabla-medica");
        if (!tabla) {
            return;
        }

        const filas = [
            ["Peso", mascota.peso_kg != null ? `${mascota.peso_kg} kg` : "—"],
            ["Altura (cruz)", mascota.altura_cm != null ? `${mascota.altura_cm} cm` : "—"],
            ["Vacunas", mascota.vacunas || "—"],
            ["Alergias", mascota.alergias || "—"],
            ["Enfermedades", mascota.enfermedades || "—"],
            ["Veterinario", mascota.veterinario || "—"],
        ];

        (mascota.eventos_medicos || []).forEach((evento) => {
            let valor = evento.descripcion || "—";
            if (evento.fecha) {
                valor += ` Fecha: ${formatearFecha(evento.fecha)}.`;
            }
            filas.push([evento.tipo || "Evento", valor]);
        });

        tabla.innerHTML = "";
        filas.forEach(([etiqueta, valor]) => {
            const fila = document.createElement("tr");
            const celdaEtiqueta = document.createElement("td");
            celdaEtiqueta.className = "label";
            celdaEtiqueta.textContent = etiqueta;

            const celdaValor = document.createElement("td");
            celdaValor.textContent = valor;

            fila.append(celdaEtiqueta, celdaValor);
            tabla.appendChild(fila);
        });
    }

    function llenarMapa(dueno) {
        const mapa = document.getElementById("mapa-dueno");
        const direccion = dueno?.contactos?.direccion?.texto;

        if (mapa && direccion) {
            mapa.src = `https://www.google.com/maps?q=${encodeURIComponent(direccion)}&z=15&output=embed`;
        }
    }

    function formatearFecha(valor) {
        const fecha = new Date(`${valor}T00:00:00`);
        if (Number.isNaN(fecha.getTime())) {
            return valor;
        }

        const texto = fecha.toLocaleDateString("es-AR", {
            month: "long",
            year: "numeric",
        });
        return texto.charAt(0).toUpperCase() + texto.slice(1);
    }

    function setTexto(id, valor) {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.textContent = valor;
        }
    }
})();
