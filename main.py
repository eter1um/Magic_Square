import sys

from PyQt6.QtWidgets import QApplication


app = QApplication(sys.argv)

from game_gui import window, start_app

start_app()

window.show()
sys.exit(app.exec())