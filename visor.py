#!/usr/bin/env python3
import sys
import os
import argparse
import requests
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout,
                             QSizePolicy, QInputDialog, QMessageBox, QFileDialog, QMenu)
from PyQt6.QtGui import QPixmap, QImage, QAction, QCursor, QActionGroup
from PyQt6.QtCore import Qt, QRect, QBuffer, QIODevice

# --- Configuración Global ---
APP_NAME = "Visor Flotante"
VERSION = "2.0"

def detach_process():
    """Desacopla el proceso de la terminal (doble fork)."""
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0)
    except OSError: sys.exit(1)

    os.setsid()

    try:
        pid = os.fork()
        if pid > 0: sys.exit(0)
    except OSError: sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'rb', 0) as f: os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'ab', 0) as f: os.dup2(f.fileno(), sys.stdout.fileno())
    with open('/dev/null', 'ab', 0) as f: os.dup2(f.fileno(), sys.stderr.fileno())

class VisorWindow(QWidget):
    def __init__(self, path_or_url):
        super().__init__()
        self.path_or_url = path_or_url
        
        # Variables de estado
        self.mouse_press_pos = None
        self.mouse_is_pressed = False
        self.edge_margin = 10
        self.resize_area = None
        self.current_scale = 1.0
        self.original_pixmap = None

        self.initUI()
        self.load_image(path_or_url)

    def initUI(self):
        # Configuración de ventana: Sin bordes, siempre visible, fondo transparente
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setAcceptDrops(True) # Habilitar Drag & Drop

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        layout.addWidget(self.label)

    def load_image(self, source):
        """Carga la imagen desde URL o Local y maneja errores."""
        image = QImage()
        try:
            if source.startswith(("http://", "https://")):
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(source, headers=headers, timeout=10)
                response.raise_for_status()
                image.loadFromData(response.content)
            else:
                local_path = source.replace("file://", "")
                local_path = os.path.expanduser(local_path)
                if not os.path.exists(local_path):
                    raise FileNotFoundError(f"Archivo no encontrado: {local_path}")
                image.load(local_path)
            
            if image.isNull():
                raise ValueError("El archivo no es una imagen válida.")

            self.original_pixmap = QPixmap.fromImage(image)
            self.path_or_url = source # Actualizar referencia actual
            self.update_display()
            
            # Ajustar tamaño inicial (max 80% pantalla)
            if self.isVisible() is False: # Solo al inicio
                screen = QApplication.primaryScreen().availableGeometry()
                w = min(self.original_pixmap.width(), screen.width() * 0.8)
                h = min(self.original_pixmap.height(), screen.height() * 0.8)
                self.resize(int(w), int(h))

        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            if not self.isVisible(): # Si falló al arrancar, salir
                sys.exit(1)

    def update_display(self):
        if self.original_pixmap:
            self.label.setPixmap(self.original_pixmap)

    # --- Eventos: Menú Contextual (Click Derecho) ---
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        # Acciones
        copy_action = QAction("Copiar al Portapapeles", self)
        copy_action.triggered.connect(self.copy_to_clipboard)
        menu.addAction(copy_action)

        save_action = QAction("Guardar como...", self)
        save_action.triggered.connect(self.save_image)
        menu.addAction(save_action)
        
        menu.addSeparator()

        # Opción de "Siempre visible"
        top_action = QAction("Siempre visible", self)
        top_action.setCheckable(True)
        top_action.setChecked(bool(self.windowFlags() & Qt.WindowType.WindowStaysOnTopHint))
        top_action.triggered.connect(self.toggle_always_on_top)
        menu.addAction(top_action)

        # Opacidad
        opacity_menu = menu.addMenu("Opacidad")
        op_group = QActionGroup(self)
        for op in [100, 75, 50, 25]:
            act = QAction(f"{op}%", self)
            act.setCheckable(True)
            if int(self.windowOpacity() * 100) == op: act.setChecked(True)
            act.triggered.connect(lambda checked, o=op: self.setWindowOpacity(o / 100))
            op_group.addAction(act)
            opacity_menu.addAction(act)

        menu.addSeparator()
        close_action = QAction("Cerrar (Salir)", self)
        close_action.triggered.connect(self.close)
        menu.addAction(close_action)

        menu.exec(event.globalPos())

    def copy_to_clipboard(self):
        if self.original_pixmap:
            QApplication.clipboard().setPixmap(self.original_pixmap)

    def save_image(self):
        if not self.original_pixmap: return
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", "imagen.png", 
                                                   "PNG (*.png);;JPG (*.jpg);;Todos (*.*)")
        if file_path:
            self.original_pixmap.save(file_path)

    def toggle_always_on_top(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    # --- Eventos: Zoom con Rueda ---
    def wheelEvent(self, event):
        # Zoom simple redimensionando la ventana
        delta = event.angleDelta().y()
        factor = 1.1 if delta > 0 else 0.9
        new_w = self.width() * factor
        new_h = self.height() * factor
        
        # Limites mínimos
        if new_w > 50 and new_h > 50:
            self.resize(int(new_w), int(new_h))

    # --- Eventos: Drag & Drop (Arrastrar archivos) ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            # Cargar el primer archivo arrastrado
            self.load_image(files[0])

    # --- Eventos: Movimiento y Redimensionado (Lógica original mejorada) ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_press_pos = event.globalPosition().toPoint()
            self.window_pos_on_click = self.pos()
            self.window_size_on_click = self.size()
            self.mouse_is_pressed = True
            self.resize_area = self._get_resize_area(event.position().toPoint())

    def mouseReleaseEvent(self, event):
        self.mouse_is_pressed = False
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseMoveEvent(self, event):
        if not self.mouse_is_pressed:
            area = self._get_resize_area(event.position().toPoint())
            self._set_cursor_shape(area)
            return
        
        delta = event.globalPosition().toPoint() - self.mouse_press_pos
        if self.resize_area:
            self._handle_resize(delta)
        else:
            self.move(self.window_pos_on_click + delta)

    def mouseDoubleClickEvent(self, event):
        # Doble click para restaurar tamaño original (1:1) o cerrar?
        # Mejor cerrar para mantener comportamiento anterior, o maximizar.
        # Mantengamos cerrar por simplicidad, pero el menú contextual es mejor.
        self.close()

    def _get_resize_area(self, pos):
        w, h = self.width(), self.height()
        m = self.edge_margin
        area = []
        if pos.x() < m: area.append("left")
        if pos.x() > w - m: area.append("right")
        if pos.y() < m: area.append("top")
        if pos.y() > h - m: area.append("bottom")
        return area if area else None

    def _set_cursor_shape(self, area):
        if not area:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            return
        
        cursors = {
            frozenset(["left", "top"]): Qt.CursorShape.SizeFDiagCursor,
            frozenset(["right", "bottom"]): Qt.CursorShape.SizeFDiagCursor,
            frozenset(["right", "top"]): Qt.CursorShape.SizeBDiagCursor,
            frozenset(["left", "bottom"]): Qt.CursorShape.SizeBDiagCursor,
            frozenset(["left"]): Qt.CursorShape.SizeHorCursor,
            frozenset(["right"]): Qt.CursorShape.SizeHorCursor,
            frozenset(["top"]): Qt.CursorShape.SizeVerCursor,
            frozenset(["bottom"]): Qt.CursorShape.SizeVerCursor
        }
        self.setCursor(cursors.get(frozenset(area), Qt.CursorShape.ArrowCursor))

    def _handle_resize(self, delta):
        rect = QRect(self.window_pos_on_click, self.window_size_on_click)
        if "right" in self.resize_area: rect.setWidth(self.window_size_on_click.width() + delta.x())
        if "bottom" in self.resize_area: rect.setHeight(self.window_size_on_click.height() + delta.y())
        if "left" in self.resize_area: rect.setLeft(self.window_pos_on_click.x() + delta.x())
        if "top" in self.resize_area: rect.setTop(self.window_pos_on_click.y() + delta.y())
        
        if rect.width() > 50 and rect.height() > 50:
            self.setGeometry(rect)

def main():
    parser = argparse.ArgumentParser(description=f"{APP_NAME} - Visualizador de imágenes flotante v{VERSION}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--target", dest="path", help="Ruta de archivo local o URL de imagen")
    group.add_argument("-p", "--popup", action="store_true", help="Abrir cuadro de diálogo para pegar URL/Ruta")
    group.add_argument("-f", "--file", action="store_true", help="Abrir explorador de archivos")
    
    parser.add_argument("-d", "--detach", action="store_true", help="Ejecutar en segundo plano y liberar terminal")

    args = parser.parse_args()

    # Lógica de Desacople (Detach)
    if args.detach:
        detach_process()

    app = QApplication(sys.argv)
    target = None

    # Lógica de selección de imagen
    if args.file:
        file_path, _ = QFileDialog.getOpenFileName(None, "Seleccionar Imagen", "", 
                                                   "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.webp)")
        target = file_path
    elif args.popup:
        text, ok = QInputDialog.getText(None, "Visor", "Introduce URL o Ruta local:")
        if ok and text:
            target = text.strip()
    elif args.path:
        target = args.path
    
    # Si no hay argumentos, mostrar ayuda o abrir selector por defecto
    if not target:
        if len(sys.argv) == 1: # Si se ejecuta solo 'visor'
             parser.print_help()
             sys.exit(0)
        else:
             sys.exit(0)

    # Iniciar ventana
    window = VisorWindow(target)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
