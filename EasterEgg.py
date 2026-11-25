from PySide6.QtWidgets import QApplication, QWidget, QLabel


class EasterEgg(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("You found a secret egg!")
        self.resize(420, 260)

        self.title = QLabel("You found a secret!", self)
        self.title.setObjectName("title")
        self.title.setGeometry(20, 20, 380, 35)

        self.hint = QLabel("Set the mass of one of the bodies to 2002 kg<br>"
                           "and its temperature to 184 °C.<br><br>"
                           "Tip: conductivity 10 makes it much faster.<br>"
                           "Then press Start and wait for the equilibrium...", self)
        self.hint.setObjectName("subtitle")
        self.hint.setGeometry(20, 70, 380, 150)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())


if __name__ == "__main__":
    app = QApplication()
    window = EasterEgg()
    window.show()
    app.exec()