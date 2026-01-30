# 👁️ Visor Flotante para Linux

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?style=flat&logo=qt)
![License](https://img.shields.io/badge/License-MIT-orange)

Un visualizador de imágenes minimalista, flotante y sin bordes diseñado para Kubuntu/Ubuntu. Ideal para mantener imágenes de referencia siempre visibles ("Always on Top") mientras trabajas, programas o estudias.

## ✨ Características

*   🖼️ **Sin bordes:** Interfaz limpia, solo ves la imagen.
*   📌 **Siempre visible:** Se mantiene por encima de otras ventanas (configurable).
*   👻 **Opacidad variable:** Ajusta la transparencia para ver a través de la imagen.
*   🖱️ **Interacción Fluida:** Mueve y redimensiona libremente.
*   🔍 **Zoom Inteligente:** Usa la rueda del ratón para escalar.
*   📂 **Drag & Drop:** Arrastra una nueva imagen sobre el visor para cambiarla al instante.
*   🚀 **Desacoplado:** Opción para liberar la terminal tras ejecutarlo.
*   🌐 **Universal:** Soporta archivos locales y URLs de internet.

## 🎮 Controles y Atajos

| Acción | Control |
| :--- | :--- |
| **Mover ventana** | `Click Izquierdo` sostenido (en el centro) + Arrastrar |
| **Redimensionar** | `Click Izquierdo` + Arrastrar desde bordes o esquinas |
| **Zoom (+ / -)** | `Rueda del Ratón` (Scroll arriba/abajo) |
| **Menú Contextual** | `Click Derecho` (Acceder a Guardar, Opacidad, Copiar, etc.) |
| **Cerrar** | `Doble Click` o `Click Derecho` -> Cerrar |
| **Cambiar imagen** | Arrastrar un archivo de imagen desde tus carpetas sobre el visor |

## 🛠️ Instalación

### Opción 1: Repositorio APT (Recomendado para actualizaciones)
Al instalarlo así, el sistema gestionará las dependencias automáticamente.
```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/Milrizos/repo/main/ ./" | sudo tee /etc/apt/sources.list.d/milrizos-repo.list
sudo apt update
sudo apt install visor
```

### Opción 2: Descarga Manual del Paquete (.deb)
Si quieres el instalador sin añadir el repositorio, descarga el paquete directamente:
1.  **Descargar:** [visor_2.0_all.deb](https://raw.githubusercontent.com/Milrizos/repo/main/pool/main/visor_2.0_all.deb)
2.  **Instalar:** Abre el archivo con el instalador de paquetes de Kubuntu (GDebi o Discover) o usa la terminal:
    ```bash
    sudo apt install ./visor_2.0_all.deb
    ```

### Opción 3: Descarga Directa del Script (Portable)
Si solo quieres el script de Python para ejecutarlo sin instalar nada en el sistema:
1.  **Descargar el script:**
    ```bash
    wget https://raw.githubusercontent.com/Milrizos/visor/main/visor.py
    ```
2.  **Instalar dependencias necesarias:**
    ```bash
    sudo apt install python3-pyqt6 python3-requests
    ```
3.  **Ejecutar:**
    ```bash
    python3 visor.py -f
    ```

## 🚀 Uso desde Terminal

Si lo instalaste vía `apt` o `.deb`, usa el comando `visor`:

* **Abrir una imagen local:** `visor -t imagen.jpg`
* **Abrir una URL:** `visor -t "https://url-de-la-imagen.png"`
* **Abrir selector de archivos:** `visor -f`
* **Modo desacoplado (liberar terminal):** `visor -d -t imagen.jpg`

---
Hecho con ❤️ por [Milrizos](https://github.com/Milrizos)
