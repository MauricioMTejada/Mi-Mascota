(async function () {
    const selector = document.getElementById("selector-mascota");
    const qrSeccion = document.getElementById("qr-mascota");
    const qrTitulo = document.getElementById("qr-mascota-titulo");
    const qrEstado = document.getElementById("qr-mascota-estado");
    const qrEnlace = document.getElementById("qr-mascota-enlace");
    const qrImagen = document.getElementById("qr-mascota-imagen");
    if (!selector || !qrSeccion || !qrTitulo || !qrEstado || !qrEnlace || !qrImagen) {
        return;
    }

    selector.addEventListener("change", () => {
        const mascotaId = selector.value;
        if (!mascotaId) {
            qrSeccion.hidden = true;
            qrImagen.removeAttribute("src");
            return;
        }

        const nombre = selector.selectedOptions[0].textContent;
        const urlFicha = new URL("ficha.html", window.location.href);
        urlFicha.searchParams.set("id", mascotaId);

        qrTitulo.textContent = `Código QR de ${nombre}`;
        qrEstado.textContent = "Generando código QR...";
        qrEnlace.href = urlFicha.href;
        qrEnlace.textContent = urlFicha.href;
        qrEnlace.hidden = true;
        qrImagen.alt = `Código QR para abrir la ficha de ${nombre}`;
        qrImagen.hidden = true;
        qrSeccion.hidden = false;
        qrImagen.src = `api/qr/mascota/${encodeURIComponent(mascotaId)}`;
    });

    qrImagen.addEventListener("load", () => {
        qrEstado.textContent = "Escanea este código con la cámara de tu teléfono.";
        qrEnlace.hidden = false;
        qrImagen.hidden = false;
    });

    qrImagen.addEventListener("error", () => {
        qrEstado.textContent = "No se pudo generar el código QR. Intenta nuevamente.";
        qrEnlace.hidden = true;
        qrImagen.hidden = true;
    });

    try {
        const respuesta = await fetch("api/mascotas", { cache: "no-store" });
        if (!respuesta.ok) {
            throw new Error(`No se pudo cargar la lista de mascotas (${respuesta.status}).`);
        }

        const mascotas = await respuesta.json();
        if (!Array.isArray(mascotas)) {
            throw new Error("La respuesta de la lista de mascotas no es válida.");
        }

        if (mascotas.length === 0) {
            selector.replaceChildren(
                new Option("No hay mascotas disponibles", "", true, true),
            );
            return;
        }

        selector.replaceChildren(new Option("Selecciona una mascota", "", true, true));
        mascotas.forEach((mascota) => {
            selector.add(new Option(mascota.nombre, mascota.id));
        });
        selector.disabled = false;
    } catch (error) {
        console.error(error);
        selector.replaceChildren(
            new Option("No se pudieron cargar las mascotas", "", true, true),
        );
    }
})();
