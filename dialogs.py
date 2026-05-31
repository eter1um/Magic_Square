from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt


def show_info_dialog(parent, title, text, ok_text, style):
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    dialog.setModal(True)
    dialog.setFixedWidth(360)
    dialog.setStyleSheet(style)

    layout = QVBoxLayout()
    dialog.setLayout(layout)

    text_label = QLabel(text)
    text_label.setWordWrap(True)
    text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    ok_button = QPushButton(ok_text)
    ok_button.setFixedSize(120, 42)
    ok_button.clicked.connect(dialog.accept)

    button_row = QHBoxLayout()
    button_row.addStretch(1)
    button_row.addWidget(ok_button)
    button_row.addStretch(1)

    layout.addSpacing(10)
    layout.addWidget(text_label)
    layout.addSpacing(14)
    layout.addLayout(button_row)
    layout.addSpacing(6)

    dialog.exec()


def show_choice_dialog(parent, title, text, left_text, right_text, style):
    result = {"choice": None}

    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    dialog.setModal(True)
    dialog.setFixedWidth(350)
    dialog.setStyleSheet(style)

    layout = QVBoxLayout()
    dialog.setLayout(layout)

    text_label = QLabel(text)
    text_label.setWordWrap(True)
    text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    left_button = QPushButton(left_text)
    right_button = QPushButton(right_text)

    left_button.setFixedSize(150, 42)
    right_button.setFixedSize(150, 42)

    def choose_left():
        result["choice"] = "left"
        dialog.accept()

    def choose_right():
        result["choice"] = "right"
        dialog.accept()

    left_button.clicked.connect(choose_left)
    right_button.clicked.connect(choose_right)

    button_row = QHBoxLayout()
    button_row.addStretch(1)
    button_row.addWidget(left_button)
    button_row.addSpacing(10)
    button_row.addWidget(right_button)
    button_row.addStretch(1)

    layout.addSpacing(10)
    layout.addWidget(text_label)
    layout.addSpacing(14)
    layout.addLayout(button_row)
    layout.addSpacing(6)

    dialog.exec()
    return result["choice"]