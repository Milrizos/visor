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

### Opción 1: Mediante mi Repositorio APT (Recomendado)
Esta es la forma más fácil. Al instalarlo así, el sistema gestionará las dependencias automáticamente y creará un acceso directo en tu menú de aplicaciones de Kubuntu.

```bash
# 1. Añadir el repositorio a tu sistema
echo "deb [trusted=yes] https://raw.githubusercontent.com/Milrizos/repo/main/ ./" | sudo tee /etc/apt/sources.list.d/milrizos-repo.list

# 2. Actualizar e instalar
sudo apt update
sudo apt install visor
