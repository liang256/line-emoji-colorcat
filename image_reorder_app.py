import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QScrollArea,
    QMessageBox,
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QPixmap, QDrag, QFont
import shutil


class ImageThumbnail(QWidget):
    def __init__(self, image_path, index, parent_window, bg_color="#cccccc"):
        super().__init__()
        self.image_path = image_path
        self.index = index
        self.parent_window = parent_window
        self.bg_color = bg_color
        self.setFixedSize(60, 80)
        self.setAcceptDrops(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        # Image
        self.image_label = QLabel()
        self.image_label.setFixedSize(56, 56)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(
            f"border: 1px solid #ccc; background-color: {bg_color};"
        )
        pixmap = QPixmap(image_path).scaled(
            50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)

        # Index label
        self.index_label = QLabel(str(index + 1))
        self.index_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(8)
        self.index_label.setFont(font)

        layout.addWidget(self.image_label)
        layout.addWidget(self.index_label)

        if index >= 40:
            overlay = QLabel(self.image_label)
            overlay.setGeometry(0, 0, 56, 56)
            overlay.setStyleSheet("background-color: rgba(100, 100, 100, 204);")
            overlay.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (
            event.position().toPoint() - self.drag_start_pos
        ).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(str(self.index))
        drag.setMimeData(mime)

        pixmap = self.image_label.pixmap()
        if pixmap:
            drag.setPixmap(
                pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

        drag.exec(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.image_label.setStyleSheet(
                "border: 2px solid #4CAF50; background-color: #e8f5e9;"
            )

    def dragLeaveEvent(self, event):
        self.image_label.setStyleSheet(
            f"border: 1px solid #ccc; background-color: {self.bg_color};"
        )

    def dropEvent(self, event):
        self.image_label.setStyleSheet(
            f"border: 1px solid #ccc; background-color: {self.bg_color};"
        )
        source_idx = int(event.mimeData().text())
        target_idx = self.index

        if source_idx != target_idx:
            self.parent_window.reorder_images(source_idx, target_idx)

        event.acceptProposedAction()


class ImageReorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Reorder Tool")
        self.setGeometry(100, 100, 1200, 800)

        self.image_paths = []
        self.thumb_bg_color = "#cccccc"

        self.init_ui()
        self.auto_load_linearts()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Buttons
        btn_layout = QVBoxLayout()

        load_btn = QPushButton("Load Images from Folder")
        load_btn.clicked.connect(self.load_folder)
        btn_layout.addWidget(load_btn)

        self.save_btn = QPushButton("Save Reordered Images")
        self.save_btn.clicked.connect(self.save_images)
        self.save_btn.setEnabled(False)
        btn_layout.addWidget(self.save_btn)

        # Background color switcher
        bg_layout = QHBoxLayout()
        bg_label = QLabel("Background:")
        bg_layout.addWidget(bg_label)
        for label, color in [("Gray", "#cccccc"), ("Red", "#e05555"), ("Blue", "#5577e0")]:
            btn = QPushButton(label)
            btn.setStyleSheet(f"background-color: {color}; color: white; font-weight: bold;")
            btn.clicked.connect(lambda _, c=color: self.set_bg_color(c))
            bg_layout.addWidget(btn)
        bg_layout.addStretch()
        btn_layout.addLayout(bg_layout)

        self.info_label = QLabel("No images loaded")
        self.info_label.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.info_label)

        layout.addLayout(btn_layout)

        # Grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        scroll.setWidget(self.grid_widget)
        layout.addWidget(scroll)

    def auto_load_linearts(self):
        linearts = Path(__file__).parent / "linearts"
        if linearts.exists() and linearts.is_dir():
            self.load_folder(str(linearts))

    def load_folder(self, folder=None):
        if not folder:
            folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if not folder:
            return

        # Load all images into the list
        images = []
        for ext in ["*.png", "*.jpg", "*.jpeg", "*.bmp"]:
            images.extend(sorted(Path(folder).glob(ext)))

        if not images:
            QMessageBox.warning(self, "No Images", "No images found in folder")
            return

        self.image_paths = [str(p) for p in images]
        self.render_grid()
        self.save_btn.setEnabled(True)
        self.info_label.setText(f"Loaded {len(self.image_paths)} images")

    def render_grid(self):
        # Clear grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Render from list
        cols = 7
        for i, path in enumerate(self.image_paths):
            row = i // cols
            col = i % cols
            thumb = ImageThumbnail(path, i, self, self.thumb_bg_color)
            self.grid_layout.addWidget(thumb, row, col)

    def set_bg_color(self, color):
        self.thumb_bg_color = color
        self.render_grid()

    def reorder_images(self, source_idx, target_idx):
        # Update the list
        item = self.image_paths.pop(source_idx)
        self.image_paths.insert(target_idx, item)

        # Re-render
        self.render_grid()

    def save_images(self):
        if not self.image_paths:
            return

        output = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not output:
            return

        # Save with new indices
        for i, path in enumerate(self.image_paths, 1):
            ext = Path(path).suffix
            new_name = f"{i:03d}{ext}"
            new_path = os.path.join(output, new_name)
            shutil.copy2(path, new_path)

        QMessageBox.information(
            self, "Success", f"Saved {len(self.image_paths)} images"
        )


def main():
    app = QApplication(sys.argv)
    window = ImageReorderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
