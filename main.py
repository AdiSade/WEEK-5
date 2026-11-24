from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                               QSlider, QDoubleSpinBox)
from PySide6.QtCore import Qt
from About import About
from Graph import Graph


class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = About()
        self.graph_window = Graph(self)     # the graph window gets access to this window
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer Simulation")
        self.resize(700, 480)

        # ---------- left body ----------
        self.left_slider = QSlider(Qt.Orientation.Vertical, self)
        self.left_slider.setGeometry(30, 40, 20, 280)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)

        self.left_body = QLabel(self)
        self.left_body.setObjectName("body")
        self.left_body.setGeometry(70, 40, 170, 280)
        self.left_body.setStyleSheet("background-color: rgb(255, 0, 0);")

        self.left_temp_label = QLabel("Temp.", self)
        self.left_temp_label.setGeometry(20, 340, 50, 30)
        self.left_temp_value = QLabel("200.0 °C", self)      # changes only through the slider
        self.left_temp_value.setObjectName("temp_value")
        self.left_temp_value.setGeometry(75, 340, 165, 30)

        self.left_mass_label = QLabel("Mass", self)
        self.left_mass_label.setGeometry(20, 380, 50, 30)
        self.left_mass_box = QDoubleSpinBox(self)
        self.left_mass_box.setGeometry(75, 380, 165, 30)
        self.left_mass_box.setRange(0.01, 10000)
        self.left_mass_box.setValue(10)
        self.left_mass_box.setSuffix(" kg")

        self.left_cap_label = QLabel("H. Cap.", self)
        self.left_cap_label.setGeometry(20, 420, 50, 30)
        self.left_cap_box = QDoubleSpinBox(self)
        self.left_cap_box.setGeometry(75, 420, 165, 30)
        self.left_cap_box.setRange(0.01, 100000)
        self.left_cap_box.setValue(1)
        self.left_cap_box.setSuffix(" J/kg°C")

        # ---------- right body ----------
        self.right_slider = QSlider(Qt.Orientation.Vertical, self)
        self.right_slider.setGeometry(650, 40, 20, 280)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)

        self.right_body = QLabel(self)
        self.right_body.setObjectName("body")
        self.right_body.setGeometry(460, 40, 170, 280)
        self.right_body.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.right_temp_value = QLabel("0.0 °C", self)
        self.right_temp_value.setObjectName("temp_value")
        self.right_temp_value.setGeometry(460, 340, 165, 30)
        self.right_temp_label = QLabel("Temp.", self)
        self.right_temp_label.setGeometry(635, 340, 55, 30)

        self.right_mass_box = QDoubleSpinBox(self)
        self.right_mass_box.setGeometry(460, 380, 165, 30)
        self.right_mass_box.setRange(0.01, 10000)
        self.right_mass_box.setValue(10)
        self.right_mass_box.setSuffix(" kg")
        self.right_mass_label = QLabel("Mass", self)
        self.right_mass_label.setGeometry(635, 380, 55, 30)

        self.right_cap_box = QDoubleSpinBox(self)
        self.right_cap_box.setGeometry(460, 420, 165, 30)
        self.right_cap_box.setRange(0.01, 100000)
        self.right_cap_box.setValue(1)
        self.right_cap_box.setSuffix(" J/kg°C")
        self.right_cap_label = QLabel("H. Cap.", self)
        self.right_cap_label.setGeometry(635, 420, 55, 30)

        # ---------- center: conductivity, bridge, buttons ----------
        self.conductivity_label = QLabel("Conductivity", self)
        self.conductivity_label.setGeometry(270, 85, 160, 25)
        self.conductivity_box = QDoubleSpinBox(self)
        self.conductivity_box.setGeometry(270, 112, 160, 30)
        self.conductivity_box.setRange(0.01, 10000)
        self.conductivity_box.setValue(1.00)
        self.conductivity_box.setSuffix(" J/s°C")

        self.bridge = QLabel(self)
        self.bridge.setObjectName("bridge")
        self.bridge.setGeometry(240, 160, 220, 60)

        self.graphs_button = QPushButton("Graphs", self)
        self.graphs_button.setGeometry(270, 40, 160, 30)
        self.graphs_button.clicked.connect(self.show_graph_window)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(270, 340, 160, 30)
        self.start_button.setCheckable(True)    # toggle button (2 states)

        self.about_button = QPushButton("About", self)
        self.about_button.setGeometry(270, 420, 160, 30)
        self.about_button.clicked.connect(self.show_about_window)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def show_about_window(self):
        self.about_window.show()

    def show_graph_window(self):
        self.graph_window.show()


if __name__ == "__main__":
    app = QApplication()
    window = HeatTransfer()
    window.show()
    app.exec()