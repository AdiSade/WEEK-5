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
        # reads the selected body from the combo box
        # adds its temperature line to the graph (does not erase the old lines)
        pass

    def clear_graph(self):
        # clears the graph and sets it up again
        pass

    def export_csv(self):
        # writes time, temperature 1, temperature 2 to a CSV file (with a header row)
        # and opens it in Excel
        pass

    def open_file(self, path):
        # opens the file with the default program
        pass


if __name__ == "__main__":
    app = QApplication()
    window = Graph(None)
    window.show()
    app.exec()