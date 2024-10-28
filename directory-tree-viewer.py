import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QPushButton, QFileDialog
)
from PyQt6.QtCore import QDir, QFileInfo
from PyQt6.QtGui import QIcon

class DirectoryTreeViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Directory Tree Viewer")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(100, 100, 800, 600)

        # Create the main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Create the directory tree widget
        self.directory_tree = QTreeWidget()
        self.directory_tree.setHeaderLabels(["Directory", "Size"])
        main_layout.addWidget(self.directory_tree)

        # Create the button to select the root directory
        select_button = QPushButton("Select Root Directory")
        select_button.clicked.connect(self.select_root_directory)
        main_layout.addWidget(select_button)

        # Set the default root directory to the current working directory
        self.root_directory = os.getcwd()
        self.populate_directory_tree(self.root_directory)

    def select_root_directory(self):
        new_root_directory = QFileDialog.getExistingDirectory(self, "Select Root Directory")
        if new_root_directory:
            self.root_directory = new_root_directory
            self.populate_directory_tree(self.root_directory)

    def populate_directory_tree(self, root_path):
        self.directory_tree.clear()
        self._add_directory_to_tree(root_path, self.directory_tree)

    def _add_directory_to_tree(self, path, parent_item):
        root_item = QTreeWidgetItem(parent_item)
        root_item.setText(0, os.path.basename(path))
        root_item.setText(1, self._get_directory_size_string(path))

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                self._add_directory_to_tree(item_path, root_item)
            else:
                file_item = QTreeWidgetItem(root_item)
                file_item.setText(0, item)
                file_item.setText(1, self._get_file_size_string(item_path))

    def _get_directory_size_string(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return self._format_size(total_size)

    def _get_file_size_string(self, path):
        return self._format_size(os.path.getsize(path))

    def _format_size(self, size):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DirectoryTreeViewer()
    window.show()
    sys.exit(app.exec())
