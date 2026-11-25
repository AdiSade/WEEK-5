import os
import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QComboBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap
from EasterEgg import EasterEgg
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class Graph(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.egg_window = EasterEgg()
        self.setWindowTitle("Heat Transfer - Graphs")
        self.resize(900, 560)

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 20, 650, 520)

        self.body_combo = QComboBox(self)
        self.body_combo.setGeometry(700, 20, 180, 34)
        self.body_combo.addItems(["Body 1", "Body 2"])

        self.draw_button = QPushButton("Draw", self)
        self.draw_button.setGeometry(700, 70, 180, 34)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(700, 120, 180, 34)

        self.export_button = QPushButton("Export to CSV", self)
        self.export_button.setGeometry(700, 170, 180, 34)
        self.egg_button = QPushButton(self)
        self.egg_button.setObjectName("egg")
        self.egg_button.setGeometry(700, 480, 60, 60)
        egg_picture = QPixmap("EASTER EGGS.jpg")
        if egg_picture.isNull():
            self.egg_button.setText("🥚")
        else:
            self.egg_button.setIcon(QIcon(egg_picture))
            self.egg_button.setIconSize(QSize(48, 48))

        self.egg_button.clicked.connect(self.show_egg_window)

        self.body1_drawn = False
        self.body2_drawn = False

        self.setup_axes()

        self.draw_button.clicked.connect(self.draw_graph)
        self.clear_button.clicked.connect(self.clear_graph)
        self.export_button.clicked.connect(self.export_csv)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def setup_axes(self):
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.set_title("Temperature over time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, color="#e0e0e0", linewidth=0.6)
        self.canvas.draw()

    def draw_graph(self):
        if len(self.main_window.time_history) == 0:
            return

        selected = self.body_combo.currentIndex()
        if selected == 0 and not self.body1_drawn:
            self.ax.plot(self.main_window.time_history, self.main_window.body1_temp_history,
                         color="red", label="Body 1")
            self.body1_drawn = True
        elif selected == 1 and not self.body2_drawn:
            self.ax.plot(self.main_window.time_history, self.main_window.body2_temp_history,
                         color="blue", label="Body 2")
            self.body2_drawn = True
        self.ax.legend()
        self.canvas.draw()

    def clear_graph(self):
        self.ax.clear()
        self.body1_drawn = False
        self.body2_drawn = False
        self.setup_axes()

    def show_egg_window(self):
        self.egg_window.show()

    def export_csv(self):
        file_name = "heat_transfer_data.csv"
        with open(file_name, "w") as f:
            f.write("time,temperature 1,temperature 2\n")
            for j in range(len(self.main_window.time_history)):
                f.write(f"{self.main_window.time_history[j]},"
                        f"{self.main_window.body1_temp_history[j]},"
                        f"{self.main_window.body2_temp_history[j]}\n")
        self.open_file(file_name)

    def open_file(self, path):
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])


if __name__ == "__main__":
    app = QApplication()
    window = Graph(None)
    window.show()
    app.exec()