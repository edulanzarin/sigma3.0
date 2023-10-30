import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel

class EmpresasMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Set the main layout margin to 0

        tab_widget = QTabWidget()
        tab_widget.setContentsMargins(0, 0, 0, 0)  # Set the QTabWidget margin to 0

        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()
        tab5 = QWidget()

        tab_widget.addTab(tab1, "Capital Six")
        tab_widget.addTab(tab2, "Grupo Lojão")
        tab_widget.addTab(tab3, "Qualitplacas")
        tab_widget.addTab(tab4, "Astral Blumenau")
        tab_widget.addTab(tab5, "Empório Astral")

        for i, tab in enumerate([tab1, tab2, tab3, tab4, tab5], start=1):
            label = QLabel(f"Content for Tab {i}")
            tab.layout = QVBoxLayout()
            tab.layout.addWidget(label)
            tab.setLayout(tab.layout)

        # Add the QTabWidget to the main layout
        layout.addWidget(tab_widget)

        # Set the layout for the main window
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = EmpresasMenu()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
