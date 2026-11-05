const botones = document.querySelectorAll('.tab-button');
const paneles = document.querySelectorAll('.tab-pane');
botones.forEach(boton => {
    boton.addEventListener('click', () => {
        const tabId = boton.dataset.tab;
        paneles.forEach(panel => panel.classList.remove('active'));
        botones.forEach(btn => btn.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        boton.classList.add('active');
    });
});