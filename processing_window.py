from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, pyqtSignal, QTimer


class ProcessingWindow(QWidget):
    updatePosition = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(150, 150)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)

        movie = QMovie(r".\assets\loading.gif")
        self.gif_label.setMovie(movie)

        movie.start()

        layout = QVBoxLayout()
        layout.addWidget(self.gif_label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)

    def update_position(self):
        if self.parent():
            x = self.parent().pos().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().pos().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)
