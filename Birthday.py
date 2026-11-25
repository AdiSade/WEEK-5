import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt, QTimer


class Birthday(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Surprise!")
        self.resize(560, 360)

        self.piece_count = 80
        self.frame = 0
        self.pieces = []
        self.pieces_x = []
        self.pieces_y = []
        self.pieces_speed_x = []
        self.pieces_speed_y = []

        for i in range(self.piece_count):
            size = np.random.randint(8, 15)
            red = np.random.randint(80, 256)
            green = np.random.randint(80, 256)
            blue = np.random.randint(80, 256)
            piece = QLabel(self)
            piece.resize(size, size)
            piece.setStyleSheet(f"background-color: rgb({red}, {green}, {blue});")
            self.pieces.append(piece)
            self.pieces_x.append(0.0)
            self.pieces_y.append(0.0)
            self.pieces_speed_x.append(0.0)
            self.pieces_speed_y.append(0.0)

        self.message = QLabel("How did you guess my birthday?", self)
        self.message.setGeometry(20, 110, 520, 100)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setStyleSheet("background: transparent; color: #ffd166; "
                                   "font-size: 30px; font-weight: bold;")

        self.caption = QLabel("No prize, but how cool is the confetti?", self)
        self.caption.setGeometry(20, 210, 520, 30)
        self.caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.caption.setStyleSheet("background: transparent; color: #9aa0b8; font-size: 13px;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.move_confetti)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def start_confetti(self):
        self.frame = 0
        for i in range(self.piece_count):
            self.pieces_x[i] = np.random.uniform(0, self.width())
            self.pieces_y[i] = np.random.uniform(-self.height(), 0)
            self.pieces_speed_x[i] = np.random.uniform(-1.5, 1.5)
            self.pieces_speed_y[i] = np.random.uniform(2, 6)
        self.timer.start(20)

    def move_confetti(self):
        self.frame += 1
        for i in range(self.piece_count):
            self.pieces_x[i] += self.pieces_speed_x[i]
            self.pieces_y[i] += self.pieces_speed_y[i]
            if self.pieces_y[i] > self.height() and self.frame < 250:
                self.pieces_y[i] = -20
            self.pieces[i].move(int(self.pieces_x[i]), int(self.pieces_y[i]))
        if self.frame > 450:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication()
    window = Birthday()
    window.show()
    window.start_confetti()
    app.exec()