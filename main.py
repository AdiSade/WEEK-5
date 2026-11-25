from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                               QSlider, QDoubleSpinBox)
from PySide6.QtCore import Qt, QTimer
from Birthday import Birthday
from Body import Body
from About import About
from Graph import Graph


class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = About()
        self.graph_window = Graph(self)
        self.birthday_window = Birthday()

        # simulation variables
        self.heat_i = 1.23
        self.dt = 0.01
        self.max_temperature = 200      # sliders, colors and the heater thermostat stop here
        self.body1 = None
        self.body2 = None
        self.counter = 0
        self.birthday_setup = False

        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        self.timer = QTimer()

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer Simulation")
        self.resize(860, 600)

        # ---------- left body ----------
        self.left_slider = QSlider(Qt.Orientation.Vertical, self)
        self.left_slider.setGeometry(45, 40, 20, 300)
        self.left_slider.setRange(0, self.max_temperature)
        self.left_slider.setValue(200)

        self.left_body = QLabel(self)
        self.left_body.setObjectName("body")
        self.left_body.setGeometry(95, 40, 195, 300)
        self.left_body.setStyleSheet("background-color: rgb(255, 0, 0);")

        self.left_temp_label = QLabel("Temp.", self)
        self.left_temp_label.setGeometry(20, 360, 70, 30)
        self.left_temp_value = QLabel("200.0 °C", self)
        self.left_temp_value.setObjectName("temp_value")
        self.left_temp_value.setGeometry(95, 360, 195, 30)

        self.left_mass_label = QLabel("Mass", self)
        self.left_mass_label.setGeometry(20, 400, 70, 30)
        self.left_mass_box = QDoubleSpinBox(self)
        self.left_mass_box.setGeometry(95, 400, 195, 30)
        self.left_mass_box.setRange(1, 10000)
        self.left_mass_box.setValue(10)
        self.left_mass_box.setSuffix(" kg")

        self.left_cap_label = QLabel("H. Cap.", self)
        self.left_cap_label.setGeometry(20, 440, 70, 30)
        self.left_cap_box = QDoubleSpinBox(self)
        self.left_cap_box.setGeometry(95, 440, 195, 30)
        self.left_cap_box.setRange(0.5, 100000)
        self.left_cap_box.setValue(1)
        self.left_cap_box.setSuffix(" J/kg°C")

        self.left_power_label = QLabel("Power", self)
        self.left_power_label.setGeometry(20, 480, 70, 30)
        self.left_power_box = QDoubleSpinBox(self)
        self.left_power_box.setGeometry(95, 480, 195, 30)
        self.left_power_box.setRange(1, 10000)
        self.left_power_box.setValue(100)
        self.left_power_box.setSuffix(" W")

        self.left_heater_button = QPushButton("Heater: OFF", self)
        self.left_heater_button.setObjectName("heater")
        self.left_heater_button.setGeometry(95, 525, 195, 34)
        self.left_heater_button.setCheckable(True)      # toggle button (2 states)

        # ---------- right body ----------
        self.right_slider = QSlider(Qt.Orientation.Vertical, self)
        self.right_slider.setGeometry(795, 40, 20, 300)
        self.right_slider.setRange(0, self.max_temperature)
        self.right_slider.setValue(0)

        self.right_body = QLabel(self)
        self.right_body.setObjectName("body")
        self.right_body.setGeometry(570, 40, 195, 300)
        self.right_body.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.right_temp_value = QLabel("0.0 °C", self)
        self.right_temp_value.setObjectName("temp_value")
        self.right_temp_value.setGeometry(570, 360, 195, 30)
        self.right_temp_label = QLabel("Temp.", self)
        self.right_temp_label.setGeometry(775, 360, 70, 30)

        self.right_mass_box = QDoubleSpinBox(self)
        self.right_mass_box.setGeometry(570, 400, 195, 30)
        self.right_mass_box.setRange(1, 10000)
        self.right_mass_box.setValue(10)
        self.right_mass_box.setSuffix(" kg")
        self.right_mass_label = QLabel("Mass", self)
        self.right_mass_label.setGeometry(775, 400, 70, 30)

        self.right_cap_box = QDoubleSpinBox(self)
        self.right_cap_box.setGeometry(570, 440, 195, 30)
        self.right_cap_box.setRange(0.5, 100000)
        self.right_cap_box.setValue(1)
        self.right_cap_box.setSuffix(" J/kg°C")
        self.right_cap_label = QLabel("H. Cap.", self)
        self.right_cap_label.setGeometry(775, 440, 70, 30)

        self.right_power_box = QDoubleSpinBox(self)
        self.right_power_box.setGeometry(570, 480, 195, 30)
        self.right_power_box.setRange(1, 10000)
        self.right_power_box.setValue(100)
        self.right_power_box.setSuffix(" W")
        self.right_power_label = QLabel("Power", self)
        self.right_power_label.setGeometry(775, 480, 70, 30)

        self.right_heater_button = QPushButton("Heater: OFF", self)
        self.right_heater_button.setObjectName("heater")
        self.right_heater_button.setGeometry(570, 525, 195, 34)
        self.right_heater_button.setCheckable(True)

        # ---------- center: conductivity, bridge, buttons ----------
        self.graphs_button = QPushButton("Graphs", self)
        self.graphs_button.setGeometry(320, 40, 220, 34)
        self.graphs_button.clicked.connect(self.show_graph_window)

        self.conductivity_label = QLabel("Conductivity", self)
        self.conductivity_label.setGeometry(320, 100, 220, 25)
        self.conductivity_box = QDoubleSpinBox(self)
        self.conductivity_box.setGeometry(320, 128, 220, 30)
        self.conductivity_box.setRange(0.01, 25)
        self.conductivity_box.setValue(1.00)
        self.conductivity_box.setSuffix(" J/s°C")

        self.bridge = QLabel(self)
        self.bridge.setObjectName("bridge")
        self.bridge.setGeometry(290, 185, 280, 60)

        self.arrows = []
        self.arrows_x = []
        for i in range(4):
            arrow = QLabel("▶", self)
            arrow.setObjectName("arrow")
            arrow.setGeometry(290 + i * 62, 195, 30, 40)
            arrow.hide()
            self.arrows.append(arrow)
            self.arrows_x.append(290 + i * 62.5)

        self.status_label = QLabel("", self)
        self.status_label.setObjectName("status")
        self.status_label.setGeometry(320, 255, 220, 45)

        self.time_label = QLabel("Time: 0.00 s", self)
        self.time_label.setObjectName("clock")
        self.time_label.setGeometry(320, 305, 220, 30)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(320, 360, 220, 34)
        self.start_button.setCheckable(True)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setGeometry(320, 405, 220, 34)
        self.reset_button.clicked.connect(self.reset_simulation)

        self.about_button = QPushButton("About", self)
        self.about_button.setGeometry(320, 450, 220, 34)
        self.about_button.clicked.connect(self.show_about_window)

        # ---------- connections ----------
        self.left_slider.valueChanged.connect(self.left_temperature_changed)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)

        self.left_heater_button.clicked.connect(self.left_heater_toggled)
        self.right_heater_button.clicked.connect(self.right_heater_toggled)

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

    def left_heater_toggled(self):
        if self.left_heater_button.isChecked():
            self.left_heater_button.setText("Heater: ON")
        else:
            self.left_heater_button.setText("Heater: OFF")

    def right_heater_toggled(self):
        if self.right_heater_button.isChecked():
            self.right_heater_button.setText("Heater: ON")
        else:
            self.right_heater_button.setText("Heater: OFF")

    def update_body_color(self, body_label, temperature):
        # 0 C = black, max temperature = full red
        red = int(temperature / self.max_temperature * 255)
        body_label.setStyleSheet(f"background-color: rgb({red}, 0, 0);")

    def show_about_window(self):
        self.about_window.show()

    def show_graph_window(self):
        self.graph_window.show()

    def show_birthday_window(self):
        self.birthday_window.start_confetti()
        self.birthday_window.show()

    def set_inputs_enabled(self, enabled):
        # the heater buttons and power boxes stay enabled, they can change while running
        self.left_slider.setEnabled(enabled)
        self.right_slider.setEnabled(enabled)
        self.left_mass_box.setEnabled(enabled)
        self.left_cap_box.setEnabled(enabled)
        self.right_mass_box.setEnabled(enabled)
        self.right_cap_box.setEnabled(enabled)
        self.conductivity_box.setEnabled(enabled)

    def move_arrows(self, temperature1, temperature2):
        difference = abs(temperature1 - temperature2)
        speed = 1 + 5 * difference / self.max_temperature
        for i in range(len(self.arrows)):
            if temperature1 > temperature2:
                self.arrows[i].setText("▶")
                self.arrows_x[i] += speed
                if self.arrows_x[i] > 540:
                    self.arrows_x[i] -= 250
            else:
                self.arrows[i].setText("◀")
                self.arrows_x[i] -= speed
                if self.arrows_x[i] < 290:
                    self.arrows_x[i] += 250
            self.arrows[i].move(int(self.arrows_x[i]), 195)
            self.arrows[i].show()

    def hide_arrows(self):
        for arrow in self.arrows:
            arrow.hide()

    def start_stop_button_method(self):
        if self.start_button.isChecked():
            self.body1 = Body(self.left_mass_box.value(), self.left_cap_box.value(), self.left_slider.value())
            self.body2 = Body(self.right_mass_box.value(), self.right_cap_box.value(), self.right_slider.value())
            self.birthday_setup = ((self.body1.mass == 2002 and self.body1.temperature == 184) or
                                   (self.body2.mass == 2002 and self.body2.temperature == 184))

            self.counter = 0
            self.time_label.setText("Time: 0.00 s")
            self.status_label.setText("")
            self.time_history.clear()
            self.body1_temp_history.clear()
            self.body2_temp_history.clear()

            self.time_history.append(0)
            self.body1_temp_history.append(self.body1.temperature)
            self.body2_temp_history.append(self.body2.temperature)

            self.set_inputs_enabled(False)
            self.timer.start(10)
            self.start_button.setText("Stop")
        else:
            self.stop_simulation()

    def timer_method(self):
        temperature1 = self.body1.temperature
        temperature2 = self.body2.temperature

        current1 = self.conductivity_box.value() * (temperature2 - temperature1)
        current2 = self.conductivity_box.value() * (temperature1 - temperature2)

        heat1 = current1 * self.dt
        heat2 = current2 * self.dt

        # heaters: power (W) * dt (s) = heat (J). A body at max temperature stops heating (thermostat)
        if self.left_heater_button.isChecked() and temperature1 < self.max_temperature:
            heat1 = heat1 + self.left_power_box.value() * self.dt
        if self.right_heater_button.isChecked() and temperature2 < self.max_temperature:
            heat2 = heat2 + self.right_power_box.value() * self.dt

        new_temperature1 = self.body1.add_heat(heat1)
        new_temperature2 = self.body2.add_heat(heat2)

        # the last step can pass the maximum, so cut it back
        if new_temperature1 > self.max_temperature:
            self.body1.temperature = self.max_temperature
            new_temperature1 = self.max_temperature
        if new_temperature2 > self.max_temperature:
            self.body2.temperature = self.max_temperature
            new_temperature2 = self.max_temperature

        self.left_slider.setValue(round(new_temperature1))
        self.left_temp_value.setText(f"{new_temperature1:.1f} °C")
        self.update_body_color(self.left_body, new_temperature1)

        self.right_slider.setValue(round(new_temperature2))
        self.right_temp_value.setText(f"{new_temperature2:.1f} °C")
        self.update_body_color(self.right_body, new_temperature2)

        self.counter += 1
        self.time_label.setText(f"Time: {self.counter * self.dt:.2f} s")
        self.time_history.append(self.counter * self.dt)
        self.body1_temp_history.append(new_temperature1)
        self.body2_temp_history.append(new_temperature2)

        self.move_arrows(new_temperature1, new_temperature2)

        # auto-stop only when no heater is on (a heated body never settles at the same temperature)
        heaters_off = not self.left_heater_button.isChecked() and not self.right_heater_button.isChecked()
        if heaters_off and abs(new_temperature1 - new_temperature2) < 0.05:
            self.status_label.setText(f"Equilibrium reached!<br>T = {new_temperature1:.1f} °C")
            self.stop_simulation()
            if self.birthday_setup:
                self.show_birthday_window()

    def stop_simulation(self):
        self.timer.stop()
        self.hide_arrows()
        self.start_button.setChecked(False)
        self.start_button.setText("Start")
        self.set_inputs_enabled(True)

    def reset_simulation(self):
        self.stop_simulation()

        self.left_slider.setValue(200)
        self.right_slider.setValue(0)
        self.left_temperature_changed()
        self.right_temperature_changed()

        self.left_mass_box.setValue(10)
        self.left_cap_box.setValue(1)
        self.right_mass_box.setValue(10)
        self.right_cap_box.setValue(1)
        self.conductivity_box.setValue(1.00)

        self.left_power_box.setValue(100)
        self.right_power_box.setValue(100)
        self.left_heater_button.setChecked(False)
        self.right_heater_button.setChecked(False)
        self.left_heater_toggled()
        self.right_heater_toggled()

        self.counter = 0
        self.time_history.clear()
        self.body1_temp_history.clear()
        self.body2_temp_history.clear()

        self.time_label.setText("Time: 0.00 s")
        self.status_label.setText("")
        self.graph_window.clear_graph()


if __name__ == "__main__":
    app = QApplication()
    window = HeatTransfer()
    window.show()
    app.exec()