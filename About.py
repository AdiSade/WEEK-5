from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QPixmap


class About(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("About - Heat Transfer")
        self.resize(340, 560)

        self.my_picture = QLabel(self)
        self.my_picture.setGeometry(70, 20, 200, 200)
        image = QPixmap("images.jpg").scaled(200, 200)
        self.my_picture.setPixmap(image)

        self.project_name = QLabel("Heat Transfer Simulation", self)
        self.project_name.setGeometry(20, 235, 300, 30)
        self.project_name.setObjectName("title")

        self.description = QLabel("Two bodies exchange heat through a<br>"
                                  "conductive bridge until they reach<br>"
                                  "the same temperature.", self)
        self.description.setGeometry(20, 275, 300, 60)
        self.description.setObjectName("subtitle")

        self.my_name = QLabel("Adi Sade", self)
        self.my_name.setGeometry(20, 360, 300, 30)

        self.my_email = QLabel("Adisade00@gmail.com", self)
        self.my_email.setGeometry(20, 395, 300, 30)

        self.my_linkedin = QLabel('<a href="https://www.linkedin.com/in/adi-sade/">My LinkedIn page</a>', self)
        self.my_linkedin.setGeometry(20, 430, 300, 30)
        self.my_linkedin.setOpenExternalLinks(True)

        self.my_github = QLabel('<a href="https://github.com/AdiSade/WEEK-5">GitHub repository</a>', self)
        self.my_github.setGeometry(20, 465, 300, 30)
        self.my_github.setOpenExternalLinks(True)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())


if __name__ == "__main__":
    app = QApplication()
    window = About()
    window.show()
    app.exec()