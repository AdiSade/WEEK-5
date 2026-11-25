from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                               QSlider, QDoubleSpinBox)
from PySide6.QtCore import Qt, QTimer
from Body import Body
from About import About
from Graph import Graph


class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = About()
        self.graph_window = Graph(self)

        # simulation variables
        self.heat_i = 1.23
        self.dt = 0.01
        self.body1 = None
        self.body2 = None
        self.counter = 0 

        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        self.timer = QTimer()

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

        self.left_slider.valueChanged.connect(self.left_temperature_changed)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)

        self.start_button.clicked.connect(self.start_stop_button_method)
        self.timer.timeout.connect(self.timer_method)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def left_temperature_changed(self):
        temperature = self.left_slider.value()
        self.left_temp_value.setText(f"{temperature:.1f} °C")
        self.update_body_color(self.left_body, temperature)

    def right_temperature_changed(self):
        temperature = self.right_slider.value()
        self.right_temp_value.setText(f"{temperature:.1f} °C")
        self.update_body_color(self.right_body, temperature)

    def update_body_color(self, body_label, temperature):
        # 0 C = black, 200 C = full red
        red = int(temperature / 200 * 255)
        body_label.setStyleSheet(f"background-color: rgb({red}, 0, 0);")
    
    def show_about_window(self):
        self.about_window.show()

    def show_graph_window(self):
        self.graph_window.show()

    def start_stop_button_method(self):
        if self.start_button.isChecked():
            self.body1 = Body(self.left_mass_box.value(), self.left_cap_box.value(), self.left_slider.value())
            self.body2 = Body(self.right_mass_box.value(), self.right_cap_box.value(), self.right_slider.value())

            self.counter = 0
            self.time_history.clear()
            self.body1_temp_history.clear()
            self.body2_temp_history.clear()

            self.time_history.append(0)
            self.body1_temp_history.append(self.body1.temperature)
            self.body2_temp_history.append(self.body2.temperature)

            self.timer.start(10)
            self.start_button.setText("Stop")
        else:
            self.timer.stop()
            self.start_button.setText("Start")

    def timer_method(self):
        temperature1 = self.body1.temperature
        temperature2 = self.body2.temperature

        current1 = self.conductivity_box.value() * (temperature2 - temperature1)
        current2 = self.conductivity_box.value() * (temperature1 - temperature2)

        heat1 = current1 * self.dt
        heat2 = current2 * self.dt

        new_temperature1 = self.body1.add_heat(heat1)
        new_temperature2 = self.body2.add_heat(heat2)

        self.left_slider.setValue(round(new_temperature1))
        self.left_temp_value.setText(f"{new_temperature1:.1f} °C")
        self.update_body_color(self.left_body, new_temperature1)

        self.right_slider.setValue(round(new_temperature2))
        self.right_temp_value.setText(f"{new_temperature2:.1f} °C")
        self.update_body_color(self.right_body, new_temperature2)

        self.counter += 1
        self.time_history.append(self.counter * self.dt)
        self.body1_temp_history.append(new_temperature1)
        self.body2_temp_history.append(new_temperature2)

if __name__ == "__main__":
    app = QApplication()
    window = HeatTransfer()
    window.show()
    app.exec()