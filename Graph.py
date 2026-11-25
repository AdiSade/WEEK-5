import os
import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QComboBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class Graph(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window      # access to the simulation data
        self.setWindowTitle("Heat Transfer - Graphs")
        self.resize(700, 420)

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 20, 480, 380)

        self.body_combo = QComboBox(self)
        self.body_combo.setGeometry(520, 20, 160, 30)
        self.body_combo.addItems(["Body 1", "Body 2"])

        self.draw_button = QPushButton("Draw", self)
        self.draw_button.setGeometry(520, 65, 160, 30)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(520, 110, 160, 30)

        self.export_button = QPushButton("Export to CSV", self)
        self.export_button.setGeometry(520, 155, 160, 30)

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
        self.canvas.draw()

    def draw_graph(self):
        selected = self.body_combo.currentIndex()
        if selected == 0:
            self.ax.plot(self.main_window.time_history, self.main_window.body1_temp_history, color="red", label="Body 1")
        else:
            self.ax.plot(self.main_window.time_history, self.main_window.body2_temp_history, color="red", label="Body 1")
        self.ax.legend()
        self.canvas.draw()

    def clear_graph(self):
        self.ax.clear()
        self.setup_axes()

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